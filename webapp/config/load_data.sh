#!/bin/bash

python3 /srv/${DJANGO_PROJECT_NAME}/manage.py loaddata actions.json
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py loaddata demographics.json
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py loaddata terms.json

python3 /srv/${DJANGO_PROJECT_NAME}/manage.py import_videos
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py score_videos
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py import_enrichments
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py score_enrichments
