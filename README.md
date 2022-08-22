# drones-api

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=ffdd54&style=for-the-badge)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![Pytest Badge](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=fff&style=for-the-badge)](https://docs.pytest.org/)

## Description

_API for drone dispatch controller using FastAPI framework in Python 3_

This API uses Repository Pattern in Hexagonal Architecture _(also known as Clean Architecture)_. Here we have two Entities: Drone and Medication, whose relationships have been exploited to create CRUD endpoints in REST under OpenAPI standard.

Some functionalities of the API:

- register/update/delete a drone
- register/update/delete a medication
- loading a drone with medication items
- checking loaded medication items for a given drone
- checking available drones for loading with pagination
- checking existing drones and medications with pagination
- check drone battery level for a given drone
- log battery level every hour

_*Note:* Check more functionalities in the API Documentation._

## Build

- Install project dependencies using [pipenv](https://pipenv.pypa.io):

  ```sh
  $ pipenv install
  ```

## Run

- Run the application:

  ```sh
  $ pipenv run python main.py
  ```

- Check the API Documentation in `localhost:8000/docs` or `localhost:8000/redoc`

## Test

- Execute Unit tests:

  ```sh
  $ pipenv run pytest
  ```
