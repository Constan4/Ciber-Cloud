#!/usr/bin/env python3
"""
misconfig_scanner.py -- Ver documentacion en el modulo correspondiente
"""
import subprocess, sys

TOOLS = {
    "azure_enum":        ["az","account","show"],
    "gcp_enum":          ["gcloud","auth","list"],
    "misconfig_scanner": ["scout","aws","--help"],
    "iam_scanner":       ["pacu","--help"],
    "container_scanner": ["trivy","--version"],
}

name = "misconfig_scanner.py".replace(".py","")
print("\n  Modulo: 05-Misconfigurations/scripts/misconfig_scanner.py")
print("  Herramientas necesarias:\n")
if "azure" in name:
    print("  az login")
    print("  az account show")
    print("  az resource list --output table")
    print("  az storage account list")
    print("  az keyvault list")
elif "gcp" in name:
    print("  gcloud auth login")
    print("  gcloud projects list")
    print("  gsutil ls")
    print("  gcloud iam service-accounts list")
elif "misconfig" in name:
    print("  pip install scoutsuite")
    print("  scout aws")
    print("  scout azure --cli")
    print("  scout gcp --user-account")
    print("  prowler -g group1")
elif "iam" in name:
    print("  pip install principalmapper")
    print("  pmapper --profile default graph create")
    print("  pmapper --profile default analysis --privesc")
    print()
    print("  pip install pacu")
    print("  pacu")
    print("  > run iam__privesc_scan")
elif "container" in name:
    print("  apt install trivy")
    print("  trivy image IMAGEN --severity HIGH,CRITICAL")
    print()
    print("  kubectl get secrets --all-namespaces -o yaml")
    print("  kubectl get pods --all-namespaces")
print()
