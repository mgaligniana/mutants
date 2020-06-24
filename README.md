# mutants

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
