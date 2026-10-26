#!/bin/bash

docker run --rm -it \
    --network=host \
    --privileged \
    --hostname "${HOSTNAME}" \
    -e MOCHA="${MOCHA:-true}" \
    -e WIFI_FALLBACK="${WIFI_FALLBACK:-true}" \
    -e WIFI_ALWAYS_ON="${WIFI_ALWAYS_ON:-false}" \
    -e WIFI_BACKUP_PERIOD="${WIFI_BACKUP_PERIOD:-10.0}" \
    -e RAJANT_TIMEOUT="${RAJANT_TIMEOUT:-10.0}" \
    -e ROBOT_CONFIGS="${ROBOT_CONFIGS:-/home/dtc/config/robot_configs.yaml}" \
    -e TOPIC_CONFIGS="${TOPIC_CONFIGS:-/home/dtc/config/topic_configs.yaml}" \
    -e RADIO_CONFIGS="${RADIO_CONFIGS:-/home/dtc/config/radio_configs.yaml}" \
    --name "dtc-platform-$(hostname)-mocha" \
    -v "$(pwd)/../config:/home/dtc/config:ro" \
    "dtc-${HOSTNAME}:mocha"
