# Selficient Python backend and API

This backend has a RESTful API to interact with the Selficient home.

_This project uses __Flask__ for the development server, unit testing support and a RESTful API._

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need:
* [Python version 3.6.x](https://www.python.org/downloads/) to create a virtual environment and install the dependencies for this project
* 'pip' and 'py' as ENVIRONMENT VARIABLES (Windows)
* [MariaDB](https://mariadb.com/downloads/) running locally on your machine

### Installing

A step by step series of examples that tell you how to get a development env running

#### Get the project from git

Clone the repo.
```
git clone https://github.com/WyTho/python_flask.git selficient-python-api
```

Change directory to the project folder
```
cd selficient-python-api
```

#### Setup a virtual environment (Windows)

[Setting up a virtual environment on Linux or MacOS](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

Install virtual environments for Python
```
py -m pip install --user virtualenv
```

Setup a virtual environment in the project folder
```
py -m virtualenv env
```

Activate the virtual environment
```
.\env\Scripts\activate
```

Optional: [More information about virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

#### Install dependencies

Install the dependencies in the virtual environment
```
pip install -r requirements.txt
```

#### Setting up the database

You should have a [MariaDB](https://mariadb.com/downloads/) instance running on your local machine.

For debugging purposes it's handy to have a GUI for the database like [HeidiSQL](https://www.heidisql.com/download.php) or [Database Workbench](https://www.upscene.com/database_workbench/). Some IDE's (like PyCharm) can connect to the database too.

Create a user for the DB with username: ```dev``` and password: ```secret```

Create a database schema called ```WySmart```

Import the database schema by running:
```
manage.py db upgrade
```

#### Optionally: Adding some fake data to the database

Run the following command to seed some dummy data into the database:
```
manage.py seed
```
This adds an example graph with its data called ```AVERAGE_TEMPERATURE```
The dummy data can be processed into averages using the Put call on ```/api/graph/AVERAGE_TEMPERATURE```

#### Starting the API
Run
```
app.py
```

## Running the tests
Run the test version of the application
```
test_app.py
```

Run in separate window
```
test_manage.py run_tests
```

# Code structure
```markdown
├── controllers (1)
├── migrations (2)
├── models (3)
├── processing (4)
└── tests (5)
```

1. `controllers` contains the resources that handle incoming requests
2. `migrations` contains the history of the database, these are used to initiate and update the database
3. `models` contains the businesslogic and database connection
4. `processing` contains scripts that are used to analyse event data in order to create graphs
5. `tests` contains the tests for this project.

## Authors

* **Rolf de Sterke** - *Initial work* - [Github page](https://github.com/RolfdeSterke)

See also the list of [contributors](https://github.com/wytho/python_flask/contributors) who participated in this project.
