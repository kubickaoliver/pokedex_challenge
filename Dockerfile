FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

# 5) Create SQLite dir and set up rights
RUN mkdir -p /data && chown -R nobody:nogroup /data

ENV DEBUG=False \
    IMPORT_POKEDEX_ON_STARTUP=True \
    IMPORT_POKEDEX_LIMIT=100 \
    API_BASE=https://pokeapi.co/api/v2

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "\
    python manage.py migrate && \
    if [ \"$IMPORT_POKEDEX_ON_STARTUP\" = \"True\" ]; then \
       python manage.py import_pokedex --limit=$IMPORT_POKEDEX_LIMIT; \
    fi && \
    gunicorn core.wsgi:application --bind 0.0.0.0:8000 \
"]