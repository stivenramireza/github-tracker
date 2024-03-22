# GitHub Tracker

GitHub tracker is a secure software application which meets some important topics about the cibersecurity like AAA (Authentication, Authorization, Accountability), DevSecOps, Infraestructure as Code (IaC), Single Point of Failure, SQL injection, Cross Site Scripting (XSS), logs, observability, alarms and CORS.

## Setup

First of all, you need to install [Python 3.12](https://www.python.org).

After that, you can create a **virtual environment** and active it in order to install the dependencies only for your propose:

```bash
$ python3.12 -m venv venv
$ source venv/bin/activate
```

### Execution

First, you need to install the main dependencies:

```bash
$ pip install --upgrade -r ./dependencies/requirements.txt
```

Later, you can run this application with the following command:

```bash
$ python main.py
```

### Testing

Some unit tests were implemented in order to validate the GitHub tracker services.

First, you need to install the test dependencies:

```bash
$ pip install --upgrade -r ./dependencies/requirements_test.txt
```

Later, you can run them and see the coverage report with the following commands:

```bash
$ coverage run -m pytest --verbose
$ coverage report -m
```
