#!/bin/bash

sudo gunicorn -b 0.0.0.0:8080 onyx.wsgi:app
