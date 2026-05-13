FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --frozen --no-dev

# Pre-download the database during build (set DB_URL in data_loader.py first)
# RUN uv run python -c "from tafsir.data_loader import get_db_path; get_db_path()"

RUN useradd --create-home --uid 1000 app && chown -R app:app /app /home/app
USER app

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "tafsir-mcp"]
