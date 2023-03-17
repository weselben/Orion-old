# My Django Project

This is a brief description of my Django project.

## Getting Started

### Prerequisites
 - Python 3.11
 - pip
 - Virtualenv

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
```sh
git clone https://github.com/weselben/orion.git
```

2. Create a virtual environment and activate it.
```sh
python -m venv env
source env/bin/activate
```

3. Install the project dependencies.
```sh
pip install -r requirements.txt
```

4. Apply the database migrations.
```sh
python manage.py migrate
```

5. Start the development server.
```sh
dotenv run python manage.py runserver
```
You should now be able to access the project at `http://localhost:8000`.

## Deployment

To deploy this project, follow these steps:

1. Set up a server with the required dependencies (e.g. Python, database server).
2. Clone the repository to the server.
```sh
git clone https://github.com/weselben/orion.git
```
3. Create a virtual environment and activate it.
```sh
python -m venv env
source env/bin/activate
```
4. Install the project dependencies.
```sh
pip install -r requirements.txt
```
5. Apply the database migrations.
```sh
python manage.py migrate
```
6. Configure your web server to serve the project (e.g. using Nginx and Gunicorn). (Port forwarding and this Shit)

7. Start the Gunicorn/Nginx server.

8. You should now be able to access the project at the server's IP address or domain name.