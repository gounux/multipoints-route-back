#!/bin/bash

source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
export APP_NAME=MPR
flask run
