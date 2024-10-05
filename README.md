# Todo API Setup

Note that if you are on Linux, any time you run a python command you should run `python <command>` instead of `py <command>`

## Environment setup

### Python

If running `py --version` in a terminal returns your version of python, you are already set up with Python. Otherwise, go to the [Python download page](https://www.python.org/downloads/) and run the installer.

Next, install venv and set up a new virtual environment in the project's directory:

```sh
pip install venv
py -m venv venv
```

The virtual environment allows us to install other Python packages in a specific directory instead of globally.

To enter the virutal environment, run one of the following:

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