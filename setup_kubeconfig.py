#!/usr/bin/env python3
import subprocess
import os
import sys

def run(cmd, capture_output=False):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        print(f"❌ Error ejecutando: {cmd}")
        sys.exit(1)
    if capture_output:
        return result.stdout.strip()

def export_kubeconfig_permanently(kubeconfig_path):
    bashrc = os.path.expanduser("~/.bashrc")
    export_line = f"export KUBECONFIG={kubeconfig_path}"

    with open(bashrc, "r") as file:
        if export_line in file.read():
            print("ℹ️  KUBECONFIG ya está en ~/.bashrc")
            return

    with open(bashrc, "a") as file:
        file.write(f"\n# Añadido automáticamente para usar kubectl con EC2\n{export_line}\n")

    print(f"✅ Añadido permanentemente a ~/.bashrc: {export_line}")

def main():
    print("🔍 Obteniendo IP pública desde Terraform...")
    ip = run("cd terraform && terraform output -raw ec2_public_ip", capture_output=True)
    print(f"✅ IP obtenida: {ip}")

    local_path = os.path.expanduser("~/.kube/k8s-ec2-config")
    remote_path = "/home/ec2-user/.kube/config"

    print("📥 Copiando archivo kubeconfig desde la instancia EC2...")
    scp_cmd = f"scp -i ~/aws.pem ec2-user@{ip}:{remote_path} {local_path}"
    run(scp_cmd)

    print(f"✅ kubeconfig copiado a: {local_path}")
    os.environ["KUBECONFIG"] = local_path

    export_kubeconfig_permanently(local_path)

    print("🔎 Ejecutando kubectl desde tu máquina local...\n")

    print("📌 kubectl get nodes")
    print(run("kubectl get nodes", capture_output=True))

    print("\n📌 kubectl get pods -A")
    print(run("kubectl get pods -A", capture_output=True))

    print("\n📌 kubectl get svc -A")
    print(run("kubectl get svc -A", capture_output=True))

    print(f"\n✅ Listo. Tu entorno está configurado.")
    print(f"   Puedes cerrar y volver a abrir la terminal o ejecutar:\n   export KUBECONFIG={local_path}")

if __name__ == "__main__":
    main()
