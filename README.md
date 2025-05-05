
# ☁️ Kubernetes en AWS EC2 Spot con Terraform + Ansible

Este proyecto crea una infraestructura completa para un clúster Kubernetes de un solo nodo en EC2 usando Terraform y Ansible.

---

## 🔧 Componentes

- **Terraform**: crea VPC, Subnet, Security Group y EC2 Spot Instance
- **Ansible**: configura containerd, Kubernetes, CNI Flannel y NGINX Ingress

---

## 📁 Estructura

```
repo-root/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
├── k8s/
│   ├── ingress.yaml
│   └── ingress-service.yaml
├── install-k8s.yml               # Playbook Ansible
├── deploy_with_ansible.sh        # Script completo
├── inventory.ini                 # Generado automáticamente
```

---

## ⚙️ Requisitos

- Terraform ≥ 1.3
- Ansible ≥ 2.10
- AWS CLI configurado
- Par de claves en AWS llamado `"aws"`
- En local: `/home/user/aws.pem` y `.pub` generado con:
  ```bash
  ssh-keygen -y -f ~/aws.pem > ~/.ssh/aws.pub
  ```

---

## 🚀 Despliegue

```bash
chmod +x deploy_with_ansible.sh
./deploy_with_ansible.sh
```

Este script:
1. Lanza la infraestructura con Terraform
2. Extrae la IP pública de la EC2
3. Genera el archivo `inventory.ini`
4. Ejecuta el playbook Ansible

---

## 🌐 Acceso

Cuando el despliegue termina, accede a:

```
http://<EC2_PUBLIC_IP>:30080/app1
```

---

## 🧼 Destrucción

Para eliminar todo:

```bash
cd terraform
terraform destroy
```

---

MIT License  
(c) 2025 Jose Magariño
