#!/bin/bash

mkdir -p /app/migrations/versions

alembic revision --autogenerate -m "Create Tables"

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 8000
