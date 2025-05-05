
# ☁️ Kubernetes en AWS EC2 Spot con Terraform + Ansible

Este proyecto despliega un clúster Kubernetes de un solo nodo usando Terraform para la infraestructura y Ansible para la configuración. La instancia EC2 es del tipo Spot para reducir costes.

---

## 📦 Tecnologías

- **Terraform**: Provisión de infraestructura (VPC, EC2, etc.)
- **Ansible**: Instalación de Kubernetes, containerd, Flannel y NGINX Ingress
- **AWS EC2 Spot**: Instancia económica (pero no persistente)

---

## 📁 Estructura

```
repo-root/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars
├── install-k8s.yml
├── deploy_with_ansible.sh
├── inventory.ini                # Se genera automáticamente
```

---

## 🧰 Requisitos previos

- Clave SSH en AWS (ej: `aws.pem`)
- Terraform ≥ 1.3
- Ansible ≥ 2.10 (`ansible --version`)
- AWS CLI configurado (`aws configure`)
- Clave pública generada:
  ```bash
  ssh-keygen -y -f ~/aws.pem > ~/.ssh/aws.pub
  ```

---

## 🚀 Despliegue completo (infraestructura + Kubernetes)

### 1. Dar permisos al script:
```bash
chmod +x deploy_with_ansible.sh
```

### 2. Ejecutar todo con un solo comando:
```bash
./deploy_with_ansible.sh
```

Esto hará automáticamente:
- Inicialización de Terraform
- Creación de VPC, SG y EC2 Spot
- Obtención de IP pública
- Generación de `inventory.ini`
- Instalación de Kubernetes + Flannel + Ingress en EC2

---

## ⏱️ Tiempo estimado de despliegue: **6–9 minutos**

| Fase                      | Tiempo aproximado |
|---------------------------|-------------------|
| Terraform infra           | ~1–2 minutos      |
| EC2 + SSH + provisión     | ~30 seg           |
| Ansible: instalar k8s     | ~4–6 minutos      |

---

## 🌐 Acceso

Una vez finalizado, accede desde el navegador:

```
http://<EC2_PUBLIC_IP>:30080
```

Obtén la IP con:

```bash
terraform output -raw ec2_public_ip
```

---

## ✅ Verificación en EC2 (opcional)

```bash
ssh -i ~/aws.pem ec2-user@<EC2_PUBLIC_IP>
kubectl get nodes
kubectl get pods -A
kubectl get svc -A
```

---

## 🧼 Eliminar toda la infraestructura

```bash
cd terraform
terraform destroy
```

Esto elimina:
- EC2
- VPC, subnets
- Security Groups

---

MIT License  
(c) 2025 Jose Magariño
