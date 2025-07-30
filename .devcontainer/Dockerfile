FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1

# ensure that any user provided certificates are installed
ARG cert_path=/usr/local/share/ca-certificates/extra
RUN --mount=type=bind,target=/mnt \
  mkdir -p $cert_path && \
  find /mnt/.devcontainer -maxdepth 1 -type f -name '*.crt' -exec install -D -t $cert_path {} \;

# ensure vscode server and python can use the user provided certificates
RUN shopt -s nullglob; certs=($cert_path/*.crt); if [ ${#certs[@]} -gt 0 ]; then cat "${certs[@]}" > "$cert_path/extra_ca_certs" && export EXTRA_CERTS="$cert_path/extra_ca_certs"; fi
ENV NODE_EXTRA_CA_CERTS=${EXTRA_CERTS:-}
ENV REQUESTS_CA_BUNDLE=${EXTRA_CERTS:-}

# ensure that the user can use a local python package repo
RUN --mount=type=bind,target=/mnt \
  find /mnt/.devcontainer -maxdepth 1 -type f -name 'pip.conf' -exec install -D {} /etc \;

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y reinstall --no-install-recommends ca-certificates software-properties-common \
    && pip install --upgrade pip \
    && pip install ipykernel jupyter

ADD https://raw.githack.com/stoplightio/prism/master/install /tmp/prism-install
RUN chmod +x /tmp/prism-install && /tmp/prism-install
