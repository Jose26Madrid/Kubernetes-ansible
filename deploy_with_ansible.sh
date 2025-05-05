#!/bin/bash
set -e

echo "➡️  Aplicando Terraform..."
cd terraform
terraform init -input=false
terraform apply -auto-approve

IP=$(terraform output -raw ec2_public_ip)
echo "📡 IP pública: $IP"

cat <<EOF > ../inventory.ini
[k8s]
$IP ansible_user=ec2-user ansible_ssh_private_key_file=~/aws.pem
EOF

echo "📁 Archivo inventory.ini generado"
cd ..
ansible-playbook -i inventory.ini install-k8s.yml
