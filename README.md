# Vendor Management System with Performance Metrics

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Madhan-raio-97/vms.git
$ cd vms
```

Create a virtual environment to install dependencies in and activate it: For Ubuntu or Mac.

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Create a virtual environment to install dependencies in and activate it: For Windows.

```sh
$ python -m venv venv
$ cd venv/scripts/
$ activate
```

Then install the dependencies:

```sh
(venv)$ cd vms
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:

Start migrations:

```sh
(env)$ cd vms
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
