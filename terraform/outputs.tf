output "db_endpoint" {
  description = "RDS connection endpoint (host:port)"
  value       = aws_db_instance.postgres.endpoint
}

output "db_address" {
  description = "RDS host only (no port)"
  value       = aws_db_instance.postgres.address
}

output "db_name" {
  value = aws_db_instance.postgres.db_name
}

output "db_port" {
  value = aws_db_instance.postgres.port
}

output "connection_string_template" {
  description = "Copy this, fill in password, put it in your .env as AIRFLOW_CONN_POSTGRES / DB_CONN_STRING"
  value       = "postgresql://${var.db_username}:<PASSWORD>@${aws_db_instance.postgres.address}:${aws_db_instance.postgres.port}/${var.db_name}"
}
