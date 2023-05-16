#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A src.tasks.celery_config:celery_app worker --loglevel=INFO
  elif [[ "${1}" == "flower" ]]; then
    celery -A src.tasks.celery_config:celery_app flower
fi
# celery -A src.tasks.celery_config:celery_app worker --loglevel=INFO
# celery -A src.tasks.celery_config:celery_app flower --port=5554
