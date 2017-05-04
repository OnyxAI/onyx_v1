#!/bin/bash

sudo gunicorn -b 0.0.0.0:80 onyx.wsgi:app
