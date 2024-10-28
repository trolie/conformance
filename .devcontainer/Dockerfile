FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

ENV PYTHONUNBUFFERED=1

COPY --chown=vscode:vscode .devcontainer/*root.pem /usr/local/share/ca-certificates/MITM.crt

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y reinstall --no-install-recommends ca-certificates software-properties-common \
    && pip install --upgrade pip \
    && pip install ipykernel jupyter

ADD https://raw.githack.com/stoplightio/prism/master/install /tmp/prism-install
RUN chmod +x /tmp/prism-install && /tmp/prism-install
