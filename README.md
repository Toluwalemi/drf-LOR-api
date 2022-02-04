# `Lord of the Rings(LOR)` API Service

`Lord of the Rings` API service is a RESTful web service that interacts with [The One API](https://the-one-api.dev/) 
to enable a user to get their favorite Lord of the Rings(LOR) characters and quotes.

## RESTFUL ROUTES

```text
|Endpoints                  |HTTP Method   |CRUDMethod   |Result   |
|---------------------------|--------------|-------------|---------|
|/characters/               |    GET       |     READ    | get all LOR characters
|/characters/:id/           |    GET       |     READ    | get a LOR character
|/signup/                   |    POST      |     CREATE  | register a user
|/login/                    |    POST      |     CREATE  | allow a user to log in
|/characters/:id/favorites  |    POST      |     CREATE  | add a favorite character
|/characters/:id/quotes/
            :id/favorites   |    POST      |     CREATE  | add a favorite character
|/characters/:id/favorites  |    GET       |     READ    | get a user's a favorite items

```

## General Usage

* Kindly run the project with Docker. 
* Clone the project.
* Create a **.env** in the project and copy the contents inside **.env-sample** into the newly
created **.env** file
* Run the docker-compose.yml file:
```bash
 docker-compose up --build
```
* Run Migrations:
```bash
 docker-compose exec web python manage.py makemigrations
 docker-compose exec web python manage.py migrate
```
* App will be available at: http://0.0.0.0:8009
* Run the tests with this command:
```bash
 docker-compose exec web pytest
```
* You may create a superuser account to add data via the django-admin:
```bash
  docker-compose exec web python manage.py createsuperuser
```