# loosely inspired by https://hynek.me/articles/docker-uv/
# but much simpler, and starting from a python base image

FROM python:3.12-slim AS build

COPY --from=ghcr.io/astral-sh/uv:latest uv usr/local/bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12 \
    UV_PROJECT_ENVIRONMENT=/app

COPY pyproject.toml /_lock/
COPY uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --locked \
    --no-dev \
    --no-install-project
EOT


FROM python:3.12-slim

ENV PATH=/app/bin:$PATH

WORKDIR /app

COPY --from=build /app ./
COPY main.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
