#!/bin/bash

alembic upgrade head

if [[ "${1}" == "prod" ]]; then
    gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --reload
elif [[ "${1}" == "dev" ]]; then
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
fi
