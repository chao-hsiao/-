# To start the web server
1. download the reprositoy
2. update and upgrade `sudo apt-get update && apt-get upgrade -y`
3. install docker `sudo apt-get install docker.io -y`
4. start the docker server `sudo systemctl start docker`
5. run the command `docker-compose up -d` in the 'docker-compose' directory to start the web server
6. open mysql server terminal `docker exec -it docker-compose_db_1 mysql --local_infile=1 -u root -p mydatabase`
7. create tables and load datasets into the database `source /queries/create_tables.sql`
8. site entry -> http://localhost:5000/
# Describtion of the web application functionality
  we use ***docker + python + mysql*** to functionize the application
1. ...
