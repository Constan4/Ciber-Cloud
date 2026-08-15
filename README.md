# ☁️ Ciber-Cloud — Cloud Security & Pentesting

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Security-FF9900?style=for-the-badge&logo=amazonaws"/>
  <img src="https://img.shields.io/badge/Azure-Security-0078D4?style=for-the-badge&logo=microsoftazure"/>
  <img src="https://img.shields.io/badge/GCP-Security-4285F4?style=for-the-badge&logo=googlecloud"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>Guia completa de seguridad ofensiva en entornos cloud.</b><br/>
  AWS, Azure, GCP — misconfiguraciones, IAM abuse, secretos expuestos y escalada de privilegios.
</p>

---

## Por que Cloud Security?

El 80% de las brechas de datos en empresas provienen de misconfiguraciones cloud.
S3 buckets publicos, IAM sin principio de minimo privilegio, secretos en codigo...
La nube ha ampliado masivamente la superficie de ataque.

---

## Kill Chain Cloud

```
  [OSINT] Descubrir activos cloud del objetivo
        |
        v
  [Reconocimiento] S3 buckets, subdominios, tecnologias cloud
        |
        v
  [Acceso inicial] SSRF -> metadatos EC2 | Credenciales expuestas | Buckets publicos
        |
        v
  [Enumeracion] IAM users, roles, politicas, recursos
        |
        v
  [Escalada] Asumir roles | Elevar privilegios IAM | Pivot entre cuentas
        |
        v
  [Exfiltracion] Datos en S3 | Secretos en SSM/Secrets Manager | RDS dumps
```

---

## Modulos

| # | Modulo | Tecnicas | Script |
|---|--------|----------|--------|
| 01 | [Reconocimiento](01-Reconocimiento/) | OSINT cloud, subdominios, buckets publicos | `cloud_recon.py` |
| 02 | [AWS](02-AWS/) | IAM enum, S3, EC2 metadata, Lambda | `aws_enum.py` |
| 03 | [Azure](03-Azure/) | Storage, Azure AD, Managed Identity | `azure_enum.py` |
| 04 | [GCP](04-GCP/) | Buckets, Service Accounts, Compute | `gcp_enum.py` |
| 05 | [Misconfiguraciones](05-Misconfigurations/) | S3 publico, SGs abiertas, sin MFA | `misconfig_scanner.py` |
| 06 | [IAM Attacks](06-IAM-Attacks/) | Privilege escalation, role chaining | `iam_scanner.py` |
| 07 | [Secrets Hunting](07-Secrets-Hunting/) | Credenciales expuestas en codigo y env | `secrets_hunter.py` |
| 08 | [Container Security](08-Container-Security/) | Docker, Kubernetes, ECR | `container_scanner.py` |

---

## Herramientas esenciales

| Herramienta | Cloud | Uso |
|-------------|-------|-----|
| **awscli** | AWS | Interactuar con todos los servicios AWS |
| **Pacu** | AWS | Framework de explotacion AWS |
| **ScoutSuite** | Multi | Auditoria de seguridad multi-cloud |
| **Prowler** | AWS | Benchmark de seguridad AWS |
| **CloudMapper** | AWS | Visualizar entornos AWS |
| **enumerate-iam** | AWS | Enumerar permisos IAM sin privilegios |
| **trufflehog** | Multi | Buscar secretos en repositorios |
| **GitLeaks** | Multi | Detectar secretos en git history |
| **az cli** | Azure | CLI oficial de Azure |
| **gcloud** | GCP | CLI oficial de GCP |

---

## Inicio rapido

```bash
# Instalar herramientas
pip install awscli pacu scoutsuite trufflehog
sudo apt install -y awscli

# Configurar credenciales AWS (si tienes)
aws configure

# Verificar identidad
aws sts get-caller-identity

# Reconocimiento de buckets S3 publicos del objetivo
python3 01-Reconocimiento/scripts/cloud_recon.py --domain objetivo.com

# Enumerar permisos IAM actuales
python3 02-AWS/scripts/aws_enum.py --enum-iam

# Buscar secretos en repositorios
python3 07-Secrets-Hunting/scripts/secrets_hunter.py --target https://github.com/objetivo
```

---

## Laboratorio

Ver [lab/setup-laboratorio.md](lab/setup-laboratorio.md)

```bash
# CloudGoat -- entorno AWS vulnerable de Rhino Security
pip install cloudgoat
cloudgoat create iam_privesc_by_attachment

# LocalStack -- AWS local sin cuenta real
pip install localstack
localstack start
```

---

## AVISO LEGAL

> Solo para uso en entornos propios o con autorizacion expresa.
> Acceder a recursos cloud sin permiso es un delito grave.

---

*Constan4 -- Cloud Security / Red Team*
