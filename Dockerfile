FROM python:3.12-slim

USER root

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USER_NAME=odoo

RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    wget \
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libevent-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    zlib1g-dev \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid=${GROUP_ID} ${USER_NAME} && \
    useradd --system --shell /bin/bash --gid=${GROUP_ID} --uid=${USER_ID} ${USER_NAME}

COPY pyproject.toml /app/pyproject.toml
WORKDIR /app
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv --no-cache sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/odoo \
    && mkdir -p /var/log/odoo \
    && mkdir -p /etc/odoo \
    && mkdir -p /usr/lib/python3/dist-packages/odoo

RUN chown -R ${USER_NAME}:${USER_NAME} /mnt/extra-addons \
    && chown -R ${USER_NAME}:${USER_NAME} /var/lib/odoo \
    && chown -R ${USER_NAME}:${USER_NAME} /var/log/odoo \
    && chown -R ${USER_NAME}:${USER_NAME} /etc/odoo \
    && chown -R ${USER_NAME}:${USER_NAME} /usr/lib/python3/dist-packages/odoo

USER ${USER_NAME}

WORKDIR /usr/lib/python3/dist-packages/odoo

EXPOSE 8069

CMD ["uv", "run", "python3", "odoo-bin", "--config=/etc/odoo/odoo.conf"]