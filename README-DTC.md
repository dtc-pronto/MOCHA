# MOCHA

MOCHA is a ROS 2 communication stack for sharing data between robots over
Rajant, with optional Wi-Fi fallback. It launches the MOCHA database,
translators, topic publishers, and Rajant interface together in one container.

The standalone container uses `MOCHA=true` to enable MOCHA. The container
hostname is passed to MOCHA as `robot_name`. If the hostname is exactly
`basestation`, it starts `basestation.launch.py`; every other hostname starts
`jackal.launch.py`.

## Parameters

| Environment variable   | Default                                 | Description                                                                    |
| ---------------------- | --------------------------------------- | ------------------------------------------------------------------------------ |
| `MOCHA`              | `true`                                | Starts MOCHA when set to `true`.                                             |
| `HOSTNAME`           | Required                                | Robot name passed to the launch file. Use `basestation` for the basestation. |
| `ROBOT_CONFIGS`      | `/home/dtc/config/robot_configs.yaml` | Robot configuration path.                                                      |
| `TOPIC_CONFIGS`      | `/home/dtc/config/topic_configs.yaml` | Topic configuration path.                                                      |
| `RADIO_CONFIGS`      | `/home/dtc/config/radio_configs.yaml` | Radio configuration path.                                                      |
| `WIFI_FALLBACK`      | `true`                                | Uses Wi-Fi when Rajant RSSI is weak or missing.                                |
| `WIFI_ALWAYS_ON`     | `false`                               | Periodically synchronizes over Wi-Fi while Rajant is healthy.                  |
| `WIFI_BACKUP_PERIOD` | `10.0`                                | Minimum seconds between Wi-Fi backup attempts per peer.                        |
| `RAJANT_TIMEOUT`     | `10.0`                                | Seconds without RSSI before Rajant is considered stale.                        |

## Docker Compose

```yaml
# version: "3.8"

x-common: &common
  ipc: host
  network_mode: host
  privileged: true
  tty: true
  logging:
    driver: local
    options:
      max-size: 100m

services:
  mocha:
    <<: *common
    init: true
    hostname: ${HOSTNAME}
    build:
      context: ./common/MOCHA
      dockerfile: Dockerfile
    image: dtc-${HOSTNAME}:mocha
    environment:
      RUN: "${MOCHA:-true}"
      WIFI_FALLBACK: "${WIFI_FALLBACK:-true}"
      WIFI_ALWAYS_ON: "${WIFI_ALWAYS_ON:-false}"
      WIFI_BACKUP_PERIOD: "${WIFI_BACKUP_PERIOD:-10.0}"
      RAJANT_TIMEOUT: "${RAJANT_TIMEOUT:-10.0}"
      ROBOT_CONFIGS: "${ROBOT_CONFIGS:-/home/dtc/config/robot_configs.yaml}"
      TOPIC_CONFIGS: "${TOPIC_CONFIGS:-/home/dtc/config/topic_configs.yaml}"
      RADIO_CONFIGS: "${RADIO_CONFIGS:-/home/dtc/config/radio_configs.yaml}"
    volumes:
      - ./common/config:/home/dtc/config:ro
```

## Example `.env`

### Basestation

```dotenv
HOSTNAME=basestation
MOCHA=true
WIFI_FALLBACK=true
WIFI_ALWAYS_ON=false
WIFI_BACKUP_PERIOD=10.0
RAJANT_TIMEOUT=10.0
```

### Ground robot

```dotenv
HOSTNAME=phobos
MOCHA=true
WIFI_FALLBACK=true
WIFI_ALWAYS_ON=false
WIFI_BACKUP_PERIOD=10.0
RAJANT_TIMEOUT=10.0
```

The configuration files must be available under `./common/config` on the host.
The image includes the Rajant watchstate JAR from this MOCHA package.
