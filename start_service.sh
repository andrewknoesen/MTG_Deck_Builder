#!/bin/bash

echo "Starting"
exec cron -f &
exec python3 main.py