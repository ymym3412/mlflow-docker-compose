#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# uncomment below when you see any issue with db...
# https://github.com/ymym3412/mlflow-docker-compose/issues/4
# mlflow db upgrade $DB_URI

mlflow server \
    --backend-store-uri $DB_URI \
    --host 0.0.0.0 \
    --port 80 \
    --default-artifact-root gs://$GCP_STORAGE_BUCKET
