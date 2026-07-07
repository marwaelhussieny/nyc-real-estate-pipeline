variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "db_name" {
  description = "Name of the Postgres database"
  type        = string
  default     = "nyc_real_estate"
}

variable "db_username" {
  description = "Master username for RDS"
  type        = string
  default     = "pipeline_admin"
}

variable "db_password" {
  description = "Master password for RDS (pass via TF_VAR_db_password env var, never commit it)"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class (db.t3.micro / db.t4g.micro is free-tier eligible)"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB (free tier covers up to 20GB)"
  type        = number
  default     = 20
}

variable "allowed_cidr" {
  description = "Your IP in CIDR form (e.g. 1.2.3.4/32) allowed to connect to Postgres. Get yours with: curl -s ifconfig.me"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "portfolio"
}
