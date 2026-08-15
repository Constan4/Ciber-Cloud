#!/usr/bin/env python3
"""
cloud_recon.py -- Reconocimiento de activos cloud via OSINT
Uso:
    python3 cloud_recon.py --domain objetivo.com
    python3 cloud_recon.py --domain objetivo.com --buckets
    python3 cloud_recon.py --domain objetivo.com --provider aws
"""
import argparse, subprocess, urllib.request, urllib.error, time

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [FOUND] "+C.RESET+m)

def check_url(url, timeout=5):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(500).decode("utf-8","ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return None, ""

def enum_s3_buckets(domain):
    info("Enumerando S3 buckets para: "+domain)
    company = domain.split(".")[0]
    variants = [
        company, company+"-backup", company+"-dev", company+"-prod",
        company+"-staging", company+"-data", company+"-files",
        company+"-logs", company+"-assets", company+"-media",
        company+"-web", company+"-app", company+"-api",
        "backup-"+company, "dev-"+company, "prod-"+company,
    ]
    found = []
    for name in variants:
        url = f"https://{name}.s3.amazonaws.com/"
        code, body = check_url(url)
        if code and code != 404:
            if code == 200 or "ListBucketResult" in body or "Contents" in body:
                crit("S3 PUBLICO: "+url+" (HTTP "+str(code)+")")
                found.append(url)
            elif code == 403:
                ok("S3 existe (privado): "+url)
            time.sleep(0.2)
    if not found:
        info("No se encontraron S3 buckets publicos")
    return found

def check_cloud_headers(domain):
    info("Analizando cabeceras cloud para: "+domain)
    url = "https://"+domain
    code, _ = check_url(url)
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            headers = dict(r.headers)
            cloud_headers = {
                "x-amz": "AWS", "x-amz-request-id": "AWS", "x-amz-id": "AWS",
                "x-azure": "Azure", "x-ms-": "Azure",
                "x-goog": "GCP", "x-cloud-trace": "GCP",
                "x-served-by": "Fastly/CDN", "x-cache": "CDN",
                "cf-ray": "Cloudflare",
            }
            detected = []
            for h_key, provider in cloud_headers.items():
                for header in headers:
                    if h_key.lower() in header.lower():
                        crit("Proveedor: "+provider+" (header: "+header+": "+headers[header][:50]+")")
                        if provider not in detected:
                            detected.append(provider)
            return detected
    except Exception:
        return []

def banner():
    print(C.BLUE+C.BOLD+"""
  ╔═══════════════════════════════════════════╗
  ║   CLOUD RECON -- OSINT de activos cloud   ║
  ╚═══════════════════════════════════════════╝
"""+C.RESET)

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--domain",   required=True)
    p.add_argument("--buckets",  action="store_true", help="Enumerar S3 buckets")
    p.add_argument("--provider", default="all", choices=["aws","azure","gcp","all"])
    args = p.parse_args()

    info("Objetivo: "+args.domain)
    print()

    check_cloud_headers(args.domain)
    print()

    if args.buckets or args.provider in ("aws","all"):
        enum_s3_buckets(args.domain)
        print()

    info("Siguientes pasos:")
    print("  trufflehog github --org ORGANIZACION --only-verified")
    print("  python3 ../07-Secrets-Hunting/scripts/secrets_hunter.py --domain "+args.domain)
    print("  scout aws  (si tienes credenciales)")

if __name__ == "__main__":
    main()
