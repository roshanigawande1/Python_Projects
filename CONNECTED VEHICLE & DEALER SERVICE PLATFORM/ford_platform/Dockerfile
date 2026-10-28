# Dockerfile
#
# Builds a container image that runs this Django API using Gunicorn (a production
# web server) — this is what gets deployed to Kubernetes in a real environment.

FROM python:3.12-slim

# Don't write .pyc files, and flush print()/logs immediately (better for container logs)
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (separate layer) so Docker can cache this step and
# skip re-installing packages every time you change your source code.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual application code.
COPY . .

# Security best practice: don't run the app as root inside the container.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Gunicorn serves config/wsgi.py's `application` object, with 3 worker processes.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
