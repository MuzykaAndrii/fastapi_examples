#!/bin/bash

alembic upgrade head

cd src

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
# uvicorn main:app --reload --host 0.0.0.0 --port 8000