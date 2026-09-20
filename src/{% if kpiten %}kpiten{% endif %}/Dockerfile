# KpiTen : one front of the dashboards (Shiny by default), on the data of the Odoo of the project.
#
# One front per image : --build-arg FRONT=shiny (5000, default), nicegui (5001) or marimo (5002).
# kpiten.dc.yml builds the three (one service per front).
#
# The code is cloned at build time, one branch per application of akretion/kpiten :
# `kpiten-core` (the library) and `<front>-kpiten`. Docker caches the clone :
# `docker compose build --no-cache kpiten-shiny kpiten-nicegui kpiten-marimo` to get the last commits.
FROM python:3.12-slim

# shiny | nicegui | marimo
ARG FRONT=shiny
ARG REPO=https://github.com/akretion/kpiten.git

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# uv : the binary of the official image (kpiten does not use pip)
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv

WORKDIR /app
# the front depends on ../kpiten-core (uv path dependency) : side by side
RUN git clone --depth 1 --branch kpiten-core "$REPO" kpiten-core \
    && git clone --depth 1 --branch "${FRONT}-kpiten" "$REPO" front

WORKDIR /app/front
# the versions of the uv.lock of the front, without the development tools
RUN uv sync --frozen --no-dev

# the parquets : a volume shared with the other fronts (see kpiten.dc.yml)
# (docky runs the container with the UID/GID of the user, without passwd nor home : HOME must
# be a writable dir, marimo looks for its configuration there)
ENV DATA_PATH=/data/kpiten HOME=/tmp
ENV PATH="/app/front/.venv/bin:$PATH"

# each front has its server and its port (5000, 5001, 5002 ; routed by traefik, see kpiten.dc.yml)
RUN case "$FRONT" in \
      shiny)   run="uvicorn shiny_kpiten.main:this_app --host 0.0.0.0 --port 5000" ;; \
      nicegui) run="python -m nicegui_kpiten.main" ;; \
      marimo)  run="uvicorn marimo_kpiten.main:this_app --host 0.0.0.0 --port 5002" ;; \
      *) echo "FRONT must be shiny, nicegui or marimo (not '$FRONT')" >&2; exit 1 ;; \
    esac \
    && printf '#!/bin/sh\nexec %s\n' "$run" > /usr/local/bin/kpiten-run \
    && chmod +x /usr/local/bin/kpiten-run

ENTRYPOINT ["kpiten-run"]
