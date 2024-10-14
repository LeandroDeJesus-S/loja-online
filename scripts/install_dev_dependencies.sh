#!/bin/sh

if [ ${ENVIRONMENT} = "development" ]; then
    pip install -r requirements-dev.txt;
fi