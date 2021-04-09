#!/bin/sh

## Sleep to give Varnish a chance to start and making sure metrics can be accessed using varnishstat command.
sleep 15 && python3 /opt/dynatrace/varnish_metrics.py $BASE_URL $API_TOKEN $APP_NAME MAIN.cache* --per-second
