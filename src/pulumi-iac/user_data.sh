#!/bin/bash

set -o errexit
set -o nounset

# user_data for aws asg launch templage 

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3 python3-pip git nginx curl

sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo usermod -aG docker ubuntu
newgrp docker

export DATABASE_URL="postgres://tododbuser:todopgpass123@10.10.5.10:5432/tododb"
cd /home/ubuntu/
git clone https://github.com/Mahboob-A/sys-design-scalable-aws-env-backend.git
cd src/
docker compose -p todo_app_backend -f dev.yml up --build -d --remove-orphans &