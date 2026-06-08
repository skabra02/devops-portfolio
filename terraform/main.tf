# Tell Terraform we're using AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Which AWS region to build in
provider "aws" {
  region = "us-east-2"
}

# Security group — the firewall rules for our server
resource "aws_security_group" "app_sg" {
  name        = "devops-portfolio-sg"
  description = "Security group for devops portfolio app"

  # Allow HTTP from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS from anywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH from anywhere (restrict to your IP in production)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "devops-portfolio-sg"
  }
}

# EC2 instance — the actual server
resource "aws_instance" "app_server" {
  ami           = "ami-0209ee5cb40d1c54b"  # Ubuntu 22.04 in us-east-2
  instance_type = "t3.micro"               # free tier eligible

  vpc_security_group_ids = [aws_security_group.app_sg.id]
  key_name               = aws_key_pair.deployer.key_name

  # Install Docker when server first boots
 user_data = <<-EOF
  #!/bin/bash
  set -e
  apt-get update -y
  apt-get install -y ca-certificates curl gnupg

  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  systemctl start docker
  systemctl enable docker
  usermod -aG docker ubuntu
EOF
  tags = {
    Name        = "devops-portfolio-server"
    Environment = "production"
    Project     = "devops-portfolio"
  }
}

# SSH key pair — so you can SSH into the server
resource "aws_key_pair" "deployer" {
  key_name   = "devops-portfolio-key"
  public_key = file("~/.ssh/id_ed25519.pub")  # your existing SSH key
}

# Elastic IP — a fixed IP address that survives server restarts
resource "aws_eip" "app_ip" {
  instance = aws_instance.app_server.id
  domain   = "vpc"

  tags = {
    Name = "devops-portfolio-eip"
  }
}
