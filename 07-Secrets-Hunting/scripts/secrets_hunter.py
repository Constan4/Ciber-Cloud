#!/usr/bin/env python3
"""
secrets_hunter.py -- Busqueda de secretos y credenciales cloud expuestas
Uso:
    python3 secrets_hunter.py --scan-dir /ruta/al/proyecto
    python3 secrets_hunter.py --repo https://github.com/objetivo/repo
    python3 secrets_hunter.py --s3 nombre-bucket --no-sign-request
"""
import argparse, os, re, subprocess

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def warn(m): print(C.YELLOW+"  [!] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [SECRET] "+C.RESET+m)

PATTERNS = {
    "AWS Access Key":    r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key":    r"(?i)aws_secret_access_key\s*[=:]\s*[A-Za-z0-9/+=]{40}",
    "AWS Session Token": r"(?i)aws_session_token\s*[=:]\s*[A-Za-z0-9/+=]{100,}",
    "Generic API Key":   r"(?i)(api_key|apikey|api-key)\s*[=:]\s*['"]([A-Za-z0-9_\-]{20,})['"]",
    "Generic Password":  r"(?i)(password|passwd|pwd)\s*[=:]\s*['"]([^'"]{8,})['"]",
    "Generic Secret":    r"(?i)(secret|token)\s*[=:]\s*['"]([A-Za-z0-9_\-]{16,})['"]",
    "Private Key":       r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----",
    "Database URL":      r"(?i)(mysql|postgres|mongodb|redis)://[^:]+:[^@]+@",
    "GitHub Token":      r"ghp_[A-Za-z0-9]{36}",
    "Slack Token":       r"xox[baprs]-[A-Za-z0-9\-]+",
    "Google API":        r"AIza[0-9A-Za-z\-_]{35}",
}

SKIP_EXTENSIONS = {".png",".jpg",".jpeg",".gif",".ico",".svg",".woff",
                   ".ttf",".eot",".pdf",".zip",".tar",".gz",".pyc"}
SKIP_DIRS = {"node_modules",".git","__pycache__",".venv","venv","dist","build"}

def scan_file(filepath):
    results = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for name, pattern in PATTERNS.items():
            matches = re.findall(pattern, content)
            if matches:
                results.append((name, filepath, matches[:3]))
    except Exception:
        pass
    return results

def scan_directory(path):
    info("Escaneando directorio: "+path)
    all_results = []
    file_count  = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue
            filepath = os.path.join(root, filename)
            results  = scan_file(filepath)
            if results:
                for name, fp, matches in results:
                    crit(name+" en "+fp.replace(path,""))
                    for m in matches:
                        print("    -> "+str(m)[:80])
                all_results.extend(results)
            file_count += 1

    print()
    info("Archivos analizados: "+str(file_count))
    if all_results:
        crit(str(len(all_results))+" secretos potenciales encontrados")
    else:
        ok("No se encontraron secretos obvios en el codigo")
    return all_results

def scan_repo(url):
    info("Clonando y escaneando: "+url)
    tmp = "/tmp/secret_scan_repo"
    subprocess.run(["rm","-rf",tmp], capture_output=True)
    r = subprocess.run(["git","clone","--depth=50",url,tmp],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        warn("Error clonando repo: "+r.stderr[:200])
        return

    scan_directory(tmp)

    info("Intentando con trufflehog (mas completo):")
    print("  trufflehog git file://"+tmp+" --only-verified")
    subprocess.run(["rm","-rf",tmp], capture_output=True)

def banner():
    print(C.GREEN+C.BOLD+"""
  ╔═══════════════════════════════════════════╗
  ║   SECRETS HUNTER -- Busqueda de secretos  ║
  ╚═══════════════════════════════════════════╝
"""+C.RESET)

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--scan-dir", default=None, help="Directorio local a escanear")
    p.add_argument("--repo",     default=None, help="URL de repositorio git")
    p.add_argument("--s3",       default=None, help="Nombre de bucket S3")
    p.add_argument("--no-sign-request", action="store_true")
    args = p.parse_args()

    if args.scan_dir:
        scan_directory(args.scan_dir)
    elif args.repo:
        scan_repo(args.repo)
    elif args.s3:
        info("Escaneando S3 bucket: "+args.s3)
        cmd = ["aws","s3","ls","--recursive","s3://"+args.s3]
        if args.no_sign_request:
            cmd.append("--no-sign-request")
        subprocess.run(cmd)
        print()
        info("Descargar archivos de configuracion:")
        for ext in [".env",".json",".yml",".yaml",".conf",".cfg",".ini"]:
            print("  aws s3 cp s3://"+args.s3+"/config"+ext+" .")
    else:
        warn("Especifica --scan-dir, --repo o --s3")
        info("Uso: python3 secrets_hunter.py --scan-dir /proyecto")

if __name__ == "__main__":
    main()
