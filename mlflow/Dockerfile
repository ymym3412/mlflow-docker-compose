ARG PYTHON_VERSION
ARG DEBIAN_VERSION
ARG TAG=${PYTHON_VERSION}-${DEBIAN_VERSION}
FROM python:${TAG}

LABEL maintainer="yu_adachi@albert2005.co.jp"
LABEL version="1.0"
LABEL description="sshとjupyterを実行可能なdocker image。付属のdocerk-composeと合わせることを推奨。"


RUN mkdir -p /mlflow/mlruns

WORKDIR /mlflow

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN echo "export LC_ALL=$LC_ALL" >> /etc/profile.d/locale.sh
RUN echo "export LANG=$LANG" >> /etc/profile.d/locale.sh

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev

RUN pip install -U pip && \
    pip install psycopg2 mlflow sqlalchemy boto3

COPY ./start.sh ./start.sh
RUN chmod +x ./start.sh

# waitライブラリの追加
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
# ライブラリの権限変更
RUN chmod +x /wait

EXPOSE 5000
