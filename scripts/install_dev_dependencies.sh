#!/bin/sh

if [ ${ENVIRONMENT} = "development" ]; then
    pip install -r requirements-dev.txt --root-user-action=ignore;
fi