
variable "public_key_path" {
  description = "Ruta a la clave pública (aws.pub)"
  type        = string
}

variable "private_key_path" {
  description = "Ruta a la clave privada (.pem)"
  type        = string
}

variable "instance_type" {
  description = "Tipo de instancia EC2 Spot"
  type        = string
  default     = "t3.large"
}
