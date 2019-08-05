# Jibrel Notable Accounts

**Jibrel Notable Accounts** provides information about Ethereum Mainnet
accounts.


## Description

Service includes a parser which scans https://etherscan.io/labelCloud/ page,
goes to lists of accounts and grabs its' names as well as aggregates labels
(Mining, Exchange, etc.).


## Prerequisites
* [Docker](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)


## Installation
```
docker-compose build
```


## Configuration
All environmental variables with its' defaults can be found in the `Dockerfile`.

> Credentials for **Proxyrack** can be found in company's **1Password** vault.


## Devtools

### Shell

To spawn a dev shell, execute:
```
make shell_tests
```

### Code validation
To check the code, you can execute the following:
```
make validate
```

The `validate` rule checks the code style, typechecks it and runs tests. If you
want to execute commands separately, check the "Code validation subrules"
section below.

### Code validation subrules

#### Linters
To run [flake8](http://flake8.pycqa.org/en/latest/), execute the following
command:
```
make lint
```

The all settings connected with a `flake8` you can customize in `.flake8`.

#### Type checking
To run [mypy](http://mypy.readthedocs.org/en/stable/) for type checking run the
following command:
```
make mypy 
```

The all settings connected with a `mypy` you can customize in `mypy.ini`.

#### Running tests
[pytest](https://pytest.org) is used as a testing framework. To run test suite,
execute: 
```
make test
```


## Author

dev@jibrel.network
