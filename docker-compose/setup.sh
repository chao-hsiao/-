#!/bin/bash

# Update and upgrade the system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install docker.io -y

# Start the Docker service
sudo systemctl start docker

# Navigate to the docker-compose directory and start the web server
sudo docker-compose up -d

# Open MySQL server terminal
# Replace 'docker-compose_db_1' with your actual Docker MySQL container name
# Replace 'mydatabase' with your actual database name
sudo docker exec -it docker-compose_db_1 mysql --local_infile=1 -u root -p mydatabase
