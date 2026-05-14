# Dockerfile for Hugging Face Space deployment.
# Mirrors the developer Dockerfile, with three deliberate changes:
#   1. Copies deploy/ in addition to src/ (for server_http.py)
#   2. Pre-downloads the 214MB DB at build time (fast cold starts)
#   3. Runs the HTTP server instead of the STDIO entry point

FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY deploy/ ./deploy/

RUN uv sync --frozen --no-dev

# HF Spaces requires UID 1000. Match the existing Dockerfile's user setup.
RUN useradd --create-home --uid 1000 app && chown -R app:app /app /home/app
USER app

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/home/app/.cache/huggingface

# Pre-download the database as the runtime user so the cache is reachable later.
# This eliminates the 30–60s download on first request.
RUN uv run python -c "from tafsir.data_loader import get_db_path; get_db_path()"

# HF Space exposes this; matches `app_port: 7860` in the Space README frontmatter.
EXPOSE 7860

CMD ["uv", "run", "python", "deploy/server_http.py"]
