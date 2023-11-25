#!/bin/bash

# Upgrade the system
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y



# Start the Docker service
sudo systemctl start docker

# Navigate to the docker-compose directory and start the web server
docker-compose up -d

# Open MySQL server terminal
# Replace 'docker-compose_db_1' with your actual Docker MySQL container name
# Replace 'mydatabase' with your actual database name
sudo docker exec -it docker-compose_db_1 mysql --local_infile=1 -u root -p mydatabase
