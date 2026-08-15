# Misconfiguraciones Cloud mas comunes

Las misconfiguraciones son la causa numero 1 de brechas de datos en cloud.

---

## AWS -- Top Misconfiguraciones

### 1. S3 Bucket publico

```bash
# Detectar
aws s3api get-bucket-acl --bucket NOMBRE
# Si aparece AllUsers o AuthenticatedUsers con permisos READ -> PUBLICO

# Impacto: cualquiera puede descargar o listar el contenido
# Remediar:
aws s3api put-bucket-acl --bucket NOMBRE --acl private
aws s3api put-public-access-block --bucket NOMBRE     --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

### 2. Security Groups abiertos (0.0.0.0/0)

```bash
# Detectar grupos con acceso desde cualquier IP
aws ec2 describe-security-groups --filters Name=ip-permission.cidr,Values="0.0.0.0/0"     --query "SecurityGroups[*].{ID:GroupId,Name:GroupName,Rules:IpPermissions}"

# Critico si permite: SSH(22), RDP(3389), MySQL(3306), Redis(6379), Elasticsearch(9200)
```

### 3. Sin MFA en cuenta root

```bash
# Verificar (requiere credenciales de root o acceso a AWS Config)
aws iam get-account-summary --query "SummaryMap.AccountMFAEnabled"
# 0 = sin MFA (critico), 1 = MFA activo

# Remediar: activar MFA virtual o fisico en la consola AWS
```

### 4. Access Keys sin rotar

```bash
# Listar access keys y su antiguedad
aws iam list-users --query "Users[*].UserName" --output text |     xargs -I {} aws iam list-access-keys --user-name {}     --query "AccessKeyMetadata[*].{User:'{}',Key:AccessKeyId,Date:CreateDate,Status:Status}"

# Keys con mas de 90 dias -> riesgo alto
```

### 5. CloudTrail deshabilitado

```bash
# Verificar si CloudTrail esta activo
aws cloudtrail describe-trails
aws cloudtrail get-trail-status --name NOMBRE

# Sin CloudTrail -> no hay logs de API calls -> el atacante no deja rastro
```

---

## Azure -- Top Misconfiguraciones

```bash
# Storage Account con acceso publico
az storage account list --query "[].{Name:name,PublicAccess:allowBlobPublicAccess}"

# VMs sin disco cifrado
az vm encryption show --name VM --resource-group RG

# Acceso de red demasiado permisivo en NSG
az network nsg rule list --nsg-name NSG --resource-group RG
```

---

## GCP -- Top Misconfiguraciones

```bash
# Buckets publicos
gsutil iam get gs://BUCKET | grep "allUsers\|allAuthenticatedUsers"

# Service accounts con demasiados permisos
gcloud projects get-iam-policy PROJECT --flatten="bindings[].members"     --filter="bindings.members:serviceAccount"     --format="table(bindings.role, bindings.members)"

# APIs innecesarias habilitadas
gcloud services list --enabled
```

---

## Script de auditoria

```bash
# Escanear misconfiguraciones automaticamente
python3 scripts/misconfig_scanner.py --provider aws --profile default
python3 scripts/misconfig_scanner.py --provider azure
python3 scripts/misconfig_scanner.py --provider gcp --project PROJECT_ID

# ScoutSuite -- auditoria completa multi-cloud
scout aws --profile default
scout azure --cli
scout gcp --user-account
```
