# mlflow-docker-compose
Deploy mlflow with docker-compose

## 1. Create .env file
In `docker-composa.yaml`, some parameters is loaded from `.env` file.
Set following parameters in `.env`.

- HOST: host name(If you don't use domain, any name is accepted. If use, speciy it)
- POSTGRES_USER: postgresql db user
- POSTGRES_PASSWORD: postgresql db user password

```
HOST=mlflow.dev
POSTGRES_USER=demo-user
POSTGRES_PASSWORD=demo-password
```

## 2. Build and deploy
Build mlflow Dockerfilw, and then deploy applications.

```sh
$ docker-compose build
$ docker-compose up -d
```
