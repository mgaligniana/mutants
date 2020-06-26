# RESTful API to detect mutants

There were completed the levels: 1, 2 and 3 (except the 'aggressive traffic' part) defined in the [challenge file](https://github.com/mgaligniana/mutants/blob/master/CHALLENGE.pdf)

## Stack used
* Flask
* PostgreSQL

## Run project

```
pip install -r requirements.txt
```

```
export FLASK_APP=app
export FLASK_ENV=development
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///mutants"
```

```
python manage.py upgrate
```

```
flask run
```

## Run tests

```
python -m unittest tests/test_api.py
```
