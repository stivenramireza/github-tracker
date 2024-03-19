# GitHub Tracker

GitHub tracker as a secure software application.

## Setup

First of all, you need to install [Python 3.12](https://www.python.org).

Later, you can create a **virtual environment** and active it in order to install the dependencies only for this project:

```bash
$ python3.10 -m venv venv
$ source venv/bin/activate
```

After that, you must install the dependencies:

```bash
pip install --upgrade -r requirements.txt
```

Now you have an environment to run this application and the automated tests.

### Execution

You can run this application with the following command:

```bash
$ python src/main.py
```

### Testing

Some unit tests were implemented in order to validate the GitHub tracker services. You can run them and see the coverage report with the following commands:

```bash
$ coverage run -m pytest --verbose
$ coverage report -m
```
