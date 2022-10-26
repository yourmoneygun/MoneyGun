#!/bin/sh

celery -A money_gun worker -l info -c $CELERY_NUM_WORKERS
