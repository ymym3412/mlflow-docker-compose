#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

mlflow server \
    --backend-store-uri $DB_URI \
    --host 0.0.0.0 \
    --port 80 \
    --default-artifact-root gs://$GCP_STORAGE_BUCKET
