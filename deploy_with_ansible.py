#!/usr/bin/env python3
import subprocess
import os
import sys

def run(cmd, capture_output=False, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Error ejecutando: {cmd}")
        sys.exit(1)
    if capture_output:
        return result.stdout.strip()

def main():
    print("📦 Paso 1: Aplicando Terraform...")
    run("terraform init -input=false", cwd="terraform")
    run("terraform apply -auto-approve", cwd="terraform")

    print("📡 Paso 2: Obteniendo IP pública...")
    ip = run("terraform output -raw ec2_public_ip", cwd="terraform", capture_output=True)
    print(f"✅ IP: {ip}")

    print("📝 Paso 3: Generando inventory.ini para Ansible...")
    inventory_path = "inventory.ini"
    with open(inventory_path, "w") as f:
        f.write(f"[k8s]\\n{ip} ansible_user=ec2-user ansible_ssh_private_key_file=~/aws.pem\\n")
    print(f"✅ inventory.ini creado")

    print("🚀 Paso 4: Ejecutando Ansible para instalar Kubernetes...")
    run(f"ansible-playbook -i {inventory_path} install-k8s.yml")

    print("📥 Paso 5: Copiando kubeconfig desde la EC2...")
    local_kubeconfig = os.path.expanduser("~/.kube/k8s-ec2-config")
    remote_path = "/home/ec2-user/.kube/config"
    run(f"scp -i ~/aws.pem ec2-user@{ip}:{remote_path} {local_kubeconfig}")

    print(f"✅ kubeconfig copiado a {local_kubeconfig}")
    os.environ["KUBECONFIG"] = local_kubeconfig

    print("🔍 Paso 6: Verificando el clúster con kubectl...\\n")
    print("📌 kubectl get nodes")
    print(run("kubectl get nodes", capture_output=True))

    print("\\n📌 kubectl get pods -A")
    print(run("kubectl get pods -A", capture_output=True))

    print("\\n📌 kubectl get svc -A")
    print(run("kubectl get svc -A", capture_output=True))

    print(f"\\n✅ Clúster desplegado correctamente. Puedes usar:")
    print(f"export KUBECONFIG={local_kubeconfig}")

if __name__ == "__main__":
    main()