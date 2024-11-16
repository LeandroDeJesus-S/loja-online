#!/bin/sh

if [ "${ENVIRONMENT}" = "development" ]; then
    pip install -r requirements-dev.txt --no-cache-dir --root-user-action=ignore;
fi