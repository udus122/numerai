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

RUN git clone --recursive \
    https://github.com/yudai1202/prezto.git \
    $HOME/.zprezto \
    && ln -s $HOME/.zprezto/runcoms/zlogin $HOME/.zlogin \
    && ln -s $HOME/.zprezto/runcoms/zlogout $HOME/.zlogout \
    && ln -s $HOME/.zprezto/runcoms/zpreztorc $HOME/.zpreztorc \
    && ln -s $HOME/.zprezto/runcoms/zprofile $HOME/.zprofile \
    && ln -s $HOME/.zprezto/runcoms/zshenv $HOME/.zshenv \
    && ln -s $HOME/.zprezto/runcoms/zshrc $HOME/.zshrc

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./

RUN pip install -U pip \
    && pip install --no-cache-dir -r requirements.txt

RUN jupyter labextension install @jupyterlab/git
# jupyer lab 3系に非対応
# && jupyter labextension install jupyterlab_filetree

WORKDIR /numerai

ADD . .

# For numerai-cli
ARG NUMERAI_PUBLIC_ID
ENV NUMERAI_PUBLIC_ID=$NUMERAI_PUBLIC_ID

ARG NUMERAI_SECRET_KEY
ENV NUMERAI_SECRET_KEY=$NUMERAI_SECRET_KEY

CMD ['python', './src/tournament/workflow/main.py']
