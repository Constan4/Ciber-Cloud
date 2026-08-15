#!/usr/bin/env python3
"""
aws_enum.py -- Enumeracion de AWS con credenciales comprometidas
Uso:
    python3 aws_enum.py --enum-iam
    python3 aws_enum.py --enum-s3
    python3 aws_enum.py --enum-all
    python3 aws_enum.py --profile nombre-perfil --enum-all
"""
import argparse, subprocess, json, sys

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def warn(m): print(C.YELLOW+"  [!] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [CRITICO] "+C.RESET+m)

def aws(cmd, profile=None):
    full_cmd = ["aws"] + cmd + ["--output","json"]
    if profile:
        full_cmd += ["--profile", profile]
    try:
        r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return json.loads(r.stdout) if r.stdout.strip() else {}
        return None
    except Exception:
        return None

def enum_identity(profile=None):
    info("Obteniendo identidad actual...")
    data = aws(["sts","get-caller-identity"], profile)
    if data:
        ok("Account: "+data.get("Account","?"))
        ok("UserId:  "+data.get("UserId","?"))
        ok("Arn:     "+data.get("Arn","?"))
        arn = data.get("Arn","")
        if "assumed-role" in arn:
            warn("Eres un rol asumido (temporal credentials)")
        elif "user" in arn:
            ok("Eres un usuario IAM permanente")
    else:
        warn("No se pudo obtener identidad. Verificar credenciales.")
        print("  aws configure")

def enum_iam(profile=None):
    info("Enumerando IAM...")

    users = aws(["iam","list-users"], profile)
    if users:
        u_list = users.get("Users",[])
        ok(str(len(u_list))+" usuarios encontrados:")
        for u in u_list:
            print("    - "+u.get("UserName","?")+" | "+u.get("Arn",""))

    roles = aws(["iam","list-roles"], profile)
    if roles:
        r_list = roles.get("Roles",[])
        ok(str(len(r_list))+" roles encontrados")
        for r in r_list[:10]:
            print("    - "+r.get("RoleName","?"))
        if len(r_list) > 10:
            print("    ... +"+str(len(r_list)-10)+" mas")

def enum_s3(profile=None):
    info("Enumerando S3 buckets...")
    data = aws(["s3api","list-buckets"], profile)
    if data:
        buckets = data.get("Buckets",[])
        ok(str(len(buckets))+" buckets encontrados:")
        for b in buckets:
            name = b.get("Name","?")
            # Check acceso publico
            acl = aws(["s3api","get-bucket-acl","--bucket",name], profile)
            public = False
            if acl:
                for grant in acl.get("Grants",[]):
                    grantee = grant.get("Grantee",{})
                    if "AllUsers" in grantee.get("URI","") or "AuthenticatedUsers" in grantee.get("URI",""):
                        public = True
            if public:
                crit("BUCKET PUBLICO: s3://"+name)
            else:
                print("    - s3://"+name+" (privado)")
    else:
        warn("Sin acceso a s3:ListBuckets")

def enum_secrets(profile=None):
    info("Buscando secretos en Secrets Manager y SSM...")

    sm = aws(["secretsmanager","list-secrets"], profile)
    if sm:
        secrets = sm.get("SecretList",[])
        if secrets:
            crit(str(len(secrets))+" secretos en Secrets Manager:")
            for s in secrets:
                print("    - "+s.get("Name","?"))
            print()
            info("Leer un secreto:")
            if secrets:
                print("    aws secretsmanager get-secret-value --secret-id "+secrets[0].get("Name","NOMBRE"))
        else:
            ok("No hay secretos en Secrets Manager")

    ssm = aws(["ssm","describe-parameters"], profile)
    if ssm:
        params = ssm.get("Parameters",[])
        if params:
            crit(str(len(params))+" parametros en SSM Parameter Store:")
            for p in params[:10]:
                print("    - "+p.get("Name","?")+" ("+p.get("Type","?")+")")
            info("Leer todos: aws ssm get-parameters-by-path --path / --recursive --with-decryption")

def banner():
    print(C.YELLOW+C.BOLD+"""
  ╔═══════════════════════════════════════════╗
  ║   AWS ENUM -- Enumeracion de AWS          ║
  ╚═══════════════════════════════════════════╝
"""+C.RESET)

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--profile",  default=None)
    p.add_argument("--enum-iam", action="store_true")
    p.add_argument("--enum-s3",  action="store_true")
    p.add_argument("--enum-secrets", action="store_true")
    p.add_argument("--enum-all", action="store_true")
    args = p.parse_args()

    enum_identity(args.profile)
    print()

    if args.enum_iam or args.enum_all:
        enum_iam(args.profile)
        print()

    if args.enum_s3 or args.enum_all:
        enum_s3(args.profile)
        print()

    if args.enum_secrets or args.enum_all:
        enum_secrets(args.profile)
        print()

if __name__ == "__main__":
    main()
