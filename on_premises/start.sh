#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

# uncomment below when you see any issue with db...
# mlflow db upgrade $DB_URI

mlflow server \
    --backend-store-uri $DB_URI \
    --host 0.0.0.0 \
    --port $VIRTUAL_PORT \
    --default-artifact-root $ARTIFACT_PATH

