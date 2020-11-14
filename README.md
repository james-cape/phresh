### Tutorial
https://www.jeffastor.com/blog/up-and-running-with-fastapi-and-docker


### Build Docker
docker-compose up -d --build

### Run Docker
docker-compose up

#### Expected request
GET http://localhost:8000/api/cleanings/

#### Expected response
[{"id":1,"name":"My house","cleaning_type":"full_clean","price_per_hour":29.99},{"id":2,"name":"Someone else's house","cleaning_type":"spot_clean","price_per_hour":19.99}]