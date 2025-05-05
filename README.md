
# ☁️ Kubernetes en AWS EC2 Spot con Terraform + Ansible + Kubectl Local

Este proyecto despliega un clúster Kubernetes de un solo nodo usando Terraform para infraestructura, Ansible para configuración, y permite interactuar con el clúster desde tu máquina local mediante `kubectl`.

---

## 📦 Tecnologías

- **Terraform**: Provisión de infraestructura (VPC, EC2 Spot, SG)
- **Ansible**: Instalación de containerd, Kubernetes, Flannel, Ingress
- **Python**: Automatiza todo el flujo
- **kubectl**: Control del clúster desde tu equipo local

---

## 📁 Estructura del proyecto

```
repo-root/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── terraform.tfvars
├── install-k8s.yml
├── deploy_all.py                  # Script completo Python
├── inventory.ini                  # Generado automáticamente
```

---

## 🧰 Requisitos

- Clave SSH (`~/aws.pem`) con permisos `chmod 400`
- Terraform ≥ 1.3
- Ansible ≥ 2.10
- Python 3 instalado
- `kubectl` instalado (`apt` o `snap`)
- AWS CLI configurado (`aws configure`)
- Clave pública generada:
  ```bash
  ssh-keygen -y -f ~/aws.pem > ~/.ssh/aws.pub
  ```

---

## 🚀 Despliegue automático completo

### 1. Dar permisos al script:

```bash
chmod +x deploy_all.py
```

### 2. Ejecutar:

```bash
./deploy_all.py
```

Este script realiza automáticamente:

1. Despliegue de infraestructura con Terraform
2. Generación del inventario Ansible
3. Instalación de Kubernetes con Ansible
4. Copia del kubeconfig a `~/.kube/k8s-ec2-config`
5. Añade automáticamente `export KUBECONFIG=~/.kube/k8s-ec2-config` a tu `~/.bashrc`
6. Ejecuta `kubectl` localmente para verificar el clúster

---

## ✅ Acceso local con kubectl

Ya puedes usar `kubectl` desde tu máquina sin configurar nada más:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get svc -A
```

El acceso persistente está configurado gracias al `export KUBECONFIG=~/.kube/k8s-ec2-config` añadido a `~/.bashrc`.

---

## ⏱ Tiempo estimado

| Fase                        | Tiempo aprox. |
|-----------------------------|---------------|
| Terraform apply             | 1–2 min       |
| Ansible (Kubernetes setup)  | 4–6 min       |
| Total                       | 6–9 min       |

---

## 🧼 Destrucción de recursos

```bash
cd terraform
terraform destroy
```

Esto elimina EC2, VPC, subnets y security groups.

---

MIT License  
(c) 2025 Jose Magariño
