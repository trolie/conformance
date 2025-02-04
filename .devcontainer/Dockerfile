FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1

# ensure that any user provided certificates are installed
ARG cert_path=/usr/local/share/ca-certificates/extra 
RUN --mount=type=bind,target=/mnt \
  mkdir -p $cert_path && \
  find /mnt/.devcontainer -maxdepth 1 -type f -name '*.crt' -exec install -D -t $cert_path {} \;
# ensure vscode can use the user provided certificates
RUN shopt -s nullglob; cat $cert_path/*.crt > $cert_path/node_extra_ca_certs
ENV NODE_EXTRA_CA_CERTS=$cert_path/node_extra_ca_certs

# ensure that the user can use a local python package repo
RUN --mount=type=bind,target=/mnt \
  find /mnt/.devcontainer -maxdepth 1 -type f -name 'pip.conf' -exec install -D {} /etc \;

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y reinstall --no-install-recommends ca-certificates software-properties-common \
    && pip install --upgrade pip \
    && pip install ipykernel jupyter

ADD https://raw.githack.com/stoplightio/prism/master/install /tmp/prism-install
RUN chmod +x /tmp/prism-install && /tmp/prism-install
