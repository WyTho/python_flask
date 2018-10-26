# python_flask

Steps to installing this program

Setting up the project itself
1. Clone the project
2. Open the project in your IDE (we're using JetBrains' Pycharm)
3. Setup the /env folder in the project as your current interpeter

Setting up the database
1. Download and install MariaDB (https://mariadb.com/downloads/)
2. Create a user for the DB with username: "dev" and password: "secret"
3. Create a database schema called "WySmart"
4. Use your terminal to run "manage.py db upgrade" from the root of the project (using the virtual env)
5. Optionally you can run "manage.py seed" to seed some dummy data into the database.
   This adds an example graph with its data called "AVERAGE_TEMPERATURE"
   The dummy data can be proccesed into averages using the Put call on "/api/graph/AVERAGE_TEMPERATURE"
