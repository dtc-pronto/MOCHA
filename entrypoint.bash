#!/bin/bash

set -e

source /opt/ros/jazzy/setup.bash
source /home/dtc/ws/install/setup.bash

if [ "${RUN}" != "true" ]; then
    exit 0
fi

WIFI_FALLBACK="${WIFI_FALLBACK:-true}"
WIFI_ALWAYS_ON="${WIFI_ALWAYS_ON:-false}"
WIFI_BACKUP_PERIOD="${WIFI_BACKUP_PERIOD:-10.0}"
RAJANT_TIMEOUT="${RAJANT_TIMEOUT:-10.0}"
ROBOT_CONFIGS="${ROBOT_CONFIGS:-/home/dtc/config/robot_configs.yaml}"
TOPIC_CONFIGS="${TOPIC_CONFIGS:-/home/dtc/config/topic_configs.yaml}"
RADIO_CONFIGS="${RADIO_CONFIGS:-/home/dtc/config/radio_configs.yaml}"

if [ "${HOSTNAME}" = "basestation" ]; then
    MOCHA_LAUNCH="basestation.launch.py"
    echo "[MOCHA] Launching MOCHA basestation"
else
    MOCHA_LAUNCH="jackal.launch.py"
    echo "[MOCHA] Launching MOCHA for ${HOSTNAME}"
fi

# log level forced to info for now
launch_args=(
    "log_level:=info"
    "robot_name:=${HOSTNAME}"
    "robot_configs:=${ROBOT_CONFIGS}"
    "topic_configs:=${TOPIC_CONFIGS}"
    "radio_configs:=${RADIO_CONFIGS}"
    "wifi_fallback_enabled:=${WIFI_FALLBACK}"
    "wifi_backup_always_on:=${WIFI_ALWAYS_ON}"
    "wifi_backup_period:=${WIFI_BACKUP_PERIOD}"
    "rajant_signal_timeout:=${RAJANT_TIMEOUT}"
)

exec ros2 launch mocha_launch "${MOCHA_LAUNCH}" "${launch_args[@]}"
