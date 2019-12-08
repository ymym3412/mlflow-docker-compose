# mlflow-docker-compose
Deploy mlflow with docker-compose

# Deploy
## 1. Login Google Cloud Platform
In this script, mlflow stores artifacts on Google Cloud Storage.  
It means you must set up GCP Credentials.  
If you already have `application_default_credentials.json`, go next chapter.  

```sh
$ gcloud auth application-default login
```
`application_default_credentials.json` will be saved `${HOME}/.config/gcloud/` 


## 2. Create .env file
In `docker-composa.yaml`, some parameters is loaded from `.env` file.  
Set following parameters in `.env`.  

- POSTGRES_USER: postgresql db user
- POSTGRES_PASSWORD: postgresql db user password
- GCP_STORAGE_BUCKET: Google Cloud Storage bucket name mlflow will store artifact
- CREDENTIALS_PATH: Path to `application_default_credentials.json`
- GCLOUD_PROJECT: GCP Project name you use

```
POSTGRES_USER=demo-user
POSTGRES_PASSWORD=demo-password
GCP_STORAGE_BUCKET=demo-bucket
CREDENTIALS_PATH=~/.config/gcloud/application_default_credentials.json
GCLOUD_PROJECT=demo-project
```

## 3. Set up NGINX Basic Authentication
Because mlflow doesn't provide authentication, use NGINX proxy for basic authentication system.  

```sh
$ sudo echo "{USER_NAME}:$(openssl passwd -apr1 {PASSWORD})" >> mlflow.localhost
```

`mlflow.localhost` is default host name.  

## 4. Build and deploy
Build mlflow Dockerfilw, and then deploy applications.  

```sh
$ docker-compose build
$ docker-compose up -d
```

# Client
To use Basic authentication, mlflow use following parameters passing HTTP authentication.  
Set following environment parameters in local,  same as [3. Set up NGINX Basic Authentication](#3-Set-up-NGINX-Basic-Authentication)

- MLFLOW_TRACKING_USERNAME
- MLFLOW_TRACKING_PASSWORD

See also https://www.mlflow.org/docs/latest/tracking.html#logging-to-a-tracking-server