we use ***docker + python + mysql*** to functionize the application
# Initialization of the web server (one time running)
1. download the repositoy
2. navigate to 'docker-compose' directory in the reposittory
3. make 'setup.sh' executable `chmod +x setup.sh`
4. execute the 'setup.sh' in 'docker-compose' directory `./setup.sh`
5. site entry -> http://localhost:5000/, http://proxmoxch.duckdns.org
# To start and stop the web server
- docker-compose up -d
- docker-compose down
# Describtion of the web application functionality
1. search: filter by various parameters to pinpoint the information you need.
2. add: easily contribute to our database by adding new property listings. fill in essential details and watch as your input becomes part of our growing collection.
3. modify: update property details, pricing, and other information directly on the search results page.
4. delete: remove outdated or incorrect entries to maintain a clean and reliable database.
