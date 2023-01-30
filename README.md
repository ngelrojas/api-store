### setup
- re-name .env.example to .env and put your config
- re-name .flaskenv.example to .flaskenv and put your config

### running docker
```shell
    docker-compose build
    docker-compose up
```

### running in docker
```shell
    docker exec it api-store-api-1 sh
```
- running flask cli

### flask cli
- flask db init -> create a directory migrations
- flask db migrate -> create files for prepare to write in postgresql
- flask db upgrade -> create a tables in postgresql