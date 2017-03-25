#!/usr/bin/env bash
sh ./start.sh client > /dev/null &
nosetests --with-coverage
