#!/bin/sh

celery -A money_gun beat -l info -S django
