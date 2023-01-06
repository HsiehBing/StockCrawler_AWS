#!/bin/bash

gunicorn -D -w 1 --access-logfile gunicorn_access.log --error-logfile gunicorn_error.log -b localhost:8080 app:app

nginx
