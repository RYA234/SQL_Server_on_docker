FROM mcr.microsoft.com/mssql/server:2022-latest

COPY . /usr/src/docker

WORKDIR /usr/src/docker
USER root
RUN apt-get update && apt-get install -y \
    sudo

RUN sudo usermod -aG root mssql
RUN chmod +x /usr/src/docker/db-init.sh

USER mssql
CMD /bin/bash ./entrypoint.sh