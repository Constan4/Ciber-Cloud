# Laboratorio de Cloud Security

---

## Opcion A -- CloudGoat (AWS vulnerable real)

CloudGoat de Rhino Security Labs crea entornos AWS intencionalmente vulnerables.
Necesitas una cuenta AWS (capa gratuita es suficiente).

```bash
pip install cloudgoat
cloudgoat config profile default

# Escenarios disponibles:
cloudgoat list

# Crear un escenario (ej: escalada de privilegios IAM)
cloudgoat create iam_privesc_by_attachment

# Destroy cuando termines (para no generar costes)
cloudgoat destroy iam_privesc_by_attachment
```

Escenarios recomendados para empezar:
- `vulnerable_lambda` -- Lambda con permisos excesivos
- `iam_privesc_by_attachment` -- escalada de privilegios IAM
- `cloud_breach_s3` -- brecha de datos via S3

---

## Opcion B -- LocalStack (sin cuenta AWS)

LocalStack simula AWS localmente. Sin coste, sin cuenta real.

```bash
pip install localstack awscli-local
localstack start

# Usar awslocal en vez de aws
awslocal s3 ls
awslocal iam list-users
awslocal s3 mb s3://test-bucket
awslocal s3api put-bucket-acl --bucket test-bucket --acl public-read
```

---

## Opcion C -- Plataformas de practica

```
HackTheBox Cloud Machines        -> maquinas con componentes cloud
TryHackMe Cloud rooms            -> rooms de AWS/Azure guiados
flaws.cloud                      -> http://flaws.cloud (AWS, gratis)
flaws2.cloud                     -> http://flaws2.cloud (AWS, gratis)
thunder-ctf.cloud.google.com     -> GCP CTF
```

flaws.cloud es el laboratorio mas recomendado para empezar con AWS.
Son 6 niveles de retos con misconfiguraciones reales de AWS.

---

## Instalacion de herramientas

```bash
# AWS CLI
sudo apt install awscli -y
# O: pip install awscli

# Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Pacu (framework de explotacion AWS)
pip install pacu

# ScoutSuite (auditoria multi-cloud)
pip install scoutsuite

# Prowler (benchmark AWS)
pip install prowler

# trufflehog (secretos en repos)
pip install trufflehog

# GitLeaks
go install github.com/gitleaks/gitleaks/v8@latest
```
