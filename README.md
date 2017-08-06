# Sunway Innovators

## Dependencies

* Flask-SQLAlchemy
* Flask-Migrate
* Flask-RESTPlus
* Flask-JWT-Extended
* Flask-CORS
* Flask-Mail
* Flask-RQ
* Flask-Script

## Setting up

##### Clone the repo

```
$ git clone https://github.com/bin4ryio/sunwayinnovators-backend.git
$ cd sunwayinnovators-backend
```

##### Initialize a virtualenv
```
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate
```
Note: if you are using a python2.x version, add an argument `-p \path\to\python3` when creating virtualenv

##### Install the dependencies

```
$(env) pip install -r requirements.txt
```

##### Create the database

```
$(env) python manage.py recreate_db
```

##### [Optional] Seed user to database

```
$(env) python manage.py seed_db
```

## Running the app

```
$(env) python manage.py runserver
```
Now navigate to [localhost:5000/docs](localhost:5000/docs) for Swagger UI


## Contributing

Contributions are welcome! Please refer to our [Code of Conduct](./CONDUCT.md) for more information.

## License
[MIT License](LICENSE.md)
