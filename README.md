# RESTful API to detect mutants

Here is the implementation for levels: 1, 2 and 3 (except the 'aggressive traffic' part) defined in the [challenge file](https://github.com/mgaligniana/mutants/blob/master/CHALLENGE.pdf)

## Stack used
* Flask
* PostgreSQL

## Run project

```
docker-compose build
docker-compose up
docker-compose run web python manage.py db upgrade
```

## Run tests

```
docker-compose run web python -m unittest tests/test_api.py
```
