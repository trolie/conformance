FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1

# ensure that any user provided certificates are installed
ENV CERT_PATH=/usr/local/share/ca-certificates/extra
RUN --mount=type=bind,target=/mnt \
  mkdir -p $CERT_PATH && \
  find /mnt/.devcontainer -maxdepth 1 -type f -name '*.crt' -exec install -D -t $CERT_PATH {} \;

# ensure vscode server and python can use the user provided certificates
RUN shopt -s nullglob; certs=($CERT_PATH/*.crt); if [ ${#certs[@]} -gt 0 ]; then cat "${certs[@]}" > "$CERT_PATH/extra_ca_certs"; fi
RUN <<EOF cat >> /etc/bash.bashrc
if [ -f "${CERT_PATH}/extra_ca_certs" ]; then
  export SSL_CERT_FILE="${CERT_PATH}/extra_ca_certs"
  export REQUESTS_CA_BUNDLE=\$SSL_CERT_FILE
  export NODE_EXTRA_CA_CERTS=\$SSL_CERT_FILE
fi
EOF
RUN . /etc/bash.bashrc

# ensure that the user can use a local python package repo
RUN --mount=type=bind,target=/mnt \
  find /mnt/.devcontainer -maxdepth 1 -type f -name 'pip.conf' -exec install -D {} /etc \;

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y reinstall --no-install-recommends ca-certificates software-properties-common \
    && pip install --upgrade pip \
    && pip install ipykernel jupyter

ADD https://raw.githack.com/stoplightio/prism/master/install /tmp/prism-install
RUN chmod +x /tmp/prism-install && /tmp/prism-install
