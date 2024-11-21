# Todo API Setup

*Note that if you are on Linux or Mac, any time you run `py <command>` you should run `python <command>` (Linux) or `python3 <command>` (Mac) instead.*

## Environment setup

### Python

If running `py --version` in a terminal returns your version of python, you are already set up with Python. Otherwise, go to the [Python download page](https://www.python.org/downloads/) and run the installer.

Next, set up a new virtual environment in the project's directory:

```sh
py -m venv venv
```

The virtual environment allows us to install other Python packages in a specific directory instead of globally. To enter the virutal environment, run one of the following:

```sh
.\venv\Scripts\activate     # Windows
source venv/bin/activate    # Linux
```

### Django

Make sure you are in the virtual environment. Then install Django and the Django REST Framework with the following commands:

```sh
pip install django
pip install django-rest-framework
```

Next, we need set up the database. Django uses a process called migrations to handle this. The Django REST Framework creates a few tables to handle user permission and authentication. To set these up, run:

```sh
py manage.py migrate
```

We also need to create our first user for the application. This will be our admin user. To do that, run:

```sh
py manage.py createsuperuser --username admin --email 'admin@example.com'
```

Django will ask you to enter a password. Use something that will be easy to remember, like `admin`. We don't really care about security right now...

## Updating the database

If you ever make changes to the models in a project, you will need to update the database, by migrating the changes. To do this, run:

```sh
py manage.py makemigrations todo
py manage.py migrate
```

The first command saves the model changes made in the todo project, and the second command applies these changes.

## Running the server

To start the Django server, make sure you are in the virtual environment and run:

```sh
py manage.py runserver
```

If you make changes to the project while the server is running, Django will automatically apply your changes.