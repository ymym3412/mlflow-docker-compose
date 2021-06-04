ARG PYTHON_VERSION
ARG DEBIAN_VERSION
ARG TAG=${PYTHON_VERSION}-${DEBIAN_VERSION}
FROM python:${TAG} AS production

LABEL maintainer="yu_adachi@albert2005.co.jp"
LABEL version="1.0"
LABEL description="sshとjupyterを実行可能なdocker image。付属のdocerk-composeと合わせることを推奨。"


RUN mkdir -p /usr/share/man/man1
# install etc & setting
RUN apt-get update -y \
    && apt-get install -y \
    wget \
    curl \
    graphviz \
    git
# install nodejs
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# install python module Production
WORKDIR /tmp/
COPY jupyter/pyproject.toml jupyter/poetry.lock* ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

# install jupyterlab extentions
RUN poetry run jupyter serverextension enable --py jupyterlab_code_formatter\
    && poetry run jupyter labextension install \
        @ryantam626/jupyterlab_code_formatter \
        @jupyterlab/toc
COPY jupyter/settings.jupyterlab-settings /root/.jupyter/lab/user-settings/@ryantam626/jupyterlab_code_formatter/settings.jupyterlab-settings

# WORKDIR /home/jovyan/work
