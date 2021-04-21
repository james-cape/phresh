### Tutorial
https://www.jeffastor.com/blog/up-and-running-with-fastapi-and-docker


### Build Docker
docker-compose up -d --build

### Run Docker
docker-compose up

## GET All Cleanings
#### Example request
GET http://localhost:8000/api/cleanings/

#### Expected Response - 200
[{"id":1,"name":"My house","cleaning_type":"full_clean","price_per_hour":29.99},{"id":2,"name":"Someone else's house","cleaning_type":"spot_clean","price_per_hour":19.99}]

## POST Create Cleaning
#### Example request
POST http://localhost:8000/api/cleanings/
```
Body: {
  "new_cleaning": {
    "name": "string",
    "description": "string",
    "price": 0,
    "cleaning_type": "spot_clean"
  }
}
```

#### Expected Response - 201
```
{
  "name": "string",
  "description": "string",
  "price": 0,
  "cleaning_type": "spot_clean",
  "id": 0
}
```
#### Expected Response - 422
```
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### Interact with Docker server container using bash commands
1. In a new Terminal run `docker ps`
1. Get the `CONTAINER ID` for the server container
1. Run `docker exec -it <CONTAINER ID> bash`
1. Try running `ls` to verify we are in the container
1. Generate a migration script with `alembic revision -m "create_main_tables"`
1. `cd app/db/migrations/versions/` and `ls` to see the newly-created migration file
1. `cd` back to the project root folder
1. Make changes to the migration file (such as creating a table)
1. Run the migrations against the database with `alembic upgrade head`
1. Verify changes in database with psql: `docker-compose exec db psql -h localhost -U postgres --dbname=postgres`
1. Run `SELECT * FROM cleanings;`
1. You should see this:
```
postgres=# SELECT * FROM cleanings;
 id | name | description | cleaning_type | price 
----+------+-------------+---------------+-------
(0 rows)
```

### Frontend
1. From `phresh/phresh-frontend`, run `yarn start` to launch frontend server