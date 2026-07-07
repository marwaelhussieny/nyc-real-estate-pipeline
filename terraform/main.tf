terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- Use the account's default VPC instead of building a new one.
# Keeps this free-tier friendly and avoids NAT gateway costs.
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_subnet_group" "this" {
  name       = "nyc-real-estate-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Project     = "nyc-real-estate-pipeline"
    Environment = var.environment
  }
}

resource "aws_security_group" "rds" {
  name        = "nyc-real-estate-rds-sg"
  description = "Allow Postgres access from a single trusted IP"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Postgres from trusted IP"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project     = "nyc-real-estate-pipeline"
    Environment = var.environment
  }
}

resource "aws_db_instance" "postgres" {
  identifier     = "nyc-real-estate-db"
  engine         = "postgres"
  engine_version = "16.4"

  instance_class        = var.db_instance_class
  allocated_storage     = var.db_allocated_storage
  storage_type          = "gp2"
  max_allocated_storage = 0 # disable autoscaling storage to stay in free tier

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = true

  # Portfolio project: prioritize teardown-ability over prod-grade durability
  skip_final_snapshot       = true
  deletion_protection       = false
  backup_retention_period   = 0
  multi_az                  = false
  apply_immediately         = true
  performance_insights_enabled = false

  tags = {
    Project     = "nyc-real-estate-pipeline"
    Environment = var.environment
  }
}
