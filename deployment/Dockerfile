FROM python:3.12-slim@sha256:80571b64ab7b94950d49d413f074e1932b65f6f75e0c34747b40ea41889a2ca9 AS base

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean


# Export python requirements from poetry
FROM base AS poetry-export

ENV PATH=$PATH:/root/.local/bin POETRY_VERSION=2.1.1
RUN curl -sSL https://install.python-poetry.org | python -
COPY ./pyproject.toml ./pyproject.toml
RUN poetry self add poetry-plugin-export
RUN poetry export --format=requirements.txt --output=requirements.txt --only=main


# Install pip requirements
# This is needed to lower the size of the final image (no build dependencies)
FROM base AS requirements

# Install requirements
RUN apt-get update && apt-get install gcc python3-dev -y --no-install-recommends
COPY --from=poetry-export requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


# Copy source code
# This is done in a separate stage to squash layers into one
FROM base AS source

RUN mkdir -p /app
WORKDIR /app
COPY wishare /app/wishare
COPY pyproject.toml /app/pyproject.toml
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations
COPY README.md /app/README.md


# Remove apt files
FROM base AS pre-final

RUN rm -rf /var/lib/apt/lists/* \
  && apt-get clean


# Final image
FROM scratch AS final

LABEL org.opencontainers.image.source=https://github.com/tanyaflos76/Flask-project

COPY --from=pre-final / /

WORKDIR /app

ENV PORT=8080 HOST=0.0.0.0

COPY --from=requirements /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=source /app /app

CMD ["python", "-m", "gunicorn", "wishare.main:app"]
