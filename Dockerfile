FROM python:3.8.6-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

RUN apt-get update && apt-get -y upgrade \
    && apt-get -y -qq --no-install-recommends install \
    curl \
    git \
    libgomp1 \
    wget \
    zsh \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /usr/local/src/*

RUN cd \
    && wget https://linux.kite.com/dls/linux/current \
    && chmod 777 current \
    && sed -i 's/"--no-launch"//g' current > /dev/null \
    && ./current --install ./kite-installer

ENV SHELL /bin/zsh

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip \
    && pip install --no-cache-dir poetry==1.0.0

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install

# RUN jupyter labextension install @jupyterlab/git
