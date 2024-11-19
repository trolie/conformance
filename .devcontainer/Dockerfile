FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

ENV PYTHONUNBUFFERED=1

RUN --mount=type=bind,target=/mnt \
  find /mnt/.devcontainer -maxdepth 1 -type f -name '*.crt' -exec install -D -t /usr/local/share/ca-certificates/extra {} \;

RUN --mount=type=bind,target=/mnt \
  find /mnt/.devcontainer -maxdepth 1 -type f -name 'pip.conf' -exec install -D {} /etc \;

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y reinstall --no-install-recommends ca-certificates software-properties-common \
    && pip install --upgrade pip \
    && pip install ipykernel jupyter

ADD https://raw.githack.com/stoplightio/prism/master/install /tmp/prism-install
RUN chmod +x /tmp/prism-install && /tmp/prism-install
