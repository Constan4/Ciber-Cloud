# Busqueda de Secretos y Credenciales Expuestas

Las credenciales cloud expuestas son el vector de ataque numero 1.

---

## Donde buscar secretos

```
Repositorios GitHub/GitLab publicos
Archivos .env commiteados por error
Variables de entorno en Lambda / ECS
Imagenes Docker en Docker Hub
Pastebins y sitios de codigo compartido
Comentarios en codigo JavaScript del frontend
Respuestas de APIs sin autenticar
S3 buckets publicos con archivos de configuracion
```

---

## GitHub Dorks para credenciales AWS

```
# Buscar en GitHub (buscador de GitHub o Google)
"AKIA" language:python
"aws_secret_access_key" filename:.env
"aws_access_key" "secret" extension:json
"amazonaws.com" "password" filename:config
org:OBJETIVO "api_key"
org:OBJETIVO "secret" language:javascript
```

---

## trufflehog -- Buscar secretos en repos

```bash
pip install trufflehog

# Escanear repo de GitHub
trufflehog github --repo https://github.com/objetivo/repo

# Escanear una organizacion entera
trufflehog github --org objetivo_org

# Escanear git local
trufflehog git file://./repo_local

# Solo resultados verificados (reduce falsos positivos)
trufflehog github --repo URL --only-verified
```

---

## GitLeaks

```bash
go install github.com/gitleaks/gitleaks/v8@latest

# Escanear repositorio local
gitleaks detect --source .

# Escanear todo el historial de commits
gitleaks detect --source . --log-opts="--all"

# Generar reporte
gitleaks detect --source . --report-path=leaks.json --report-format=json
```

---

## Verificar si las credenciales AWS son validas

```bash
# Una vez encontrado AKID + SECRET
aws configure set aws_access_key_id AKID
aws configure set aws_secret_access_key SECRET

# Verificar sin hacer ruido
aws sts get-caller-identity

# Si funciona -> tenemos acceso
# Ver que permisos tiene
python3 enumerate-iam.py --access-key AKID --secret-key SECRET
```

---

## Buscar secretos en imagenes Docker

```bash
# Descargar imagen y analizar capas
docker pull objetivo/imagen:latest
docker history objetivo/imagen:latest --no-trunc

# Extraer el sistema de archivos
docker save objetivo/imagen > imagen.tar
mkdir layers && tar xf imagen.tar -C layers

# Buscar secretos en los archivos
grep -r "password\|secret\|api_key\|token" layers/ 2>/dev/null
grep -r "AKIA\|AWS_" layers/ 2>/dev/null

# dive -- herramienta grafica para inspeccionar capas
dive objetivo/imagen:latest
```

---

## Script propio

```bash
python3 scripts/secrets_hunter.py --github-org objetivo_org
python3 scripts/secrets_hunter.py --repo https://github.com/objetivo/repo
python3 scripts/secrets_hunter.py --docker-image objetivo/imagen
python3 scripts/secrets_hunter.py --s3-bucket objetivo-dev --no-sign-request
```
