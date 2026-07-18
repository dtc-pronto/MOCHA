☕ MOCHA: Multi-robot Opportunistic Communication for Heterogeneous Collaboration
---------------------------------------------------------------------------------
![MOCHA gif](mocha.gif)

This repository contains the distributed and opportunistic communication stack used for multi-robot experiments at KumarRobotics.

## Directories

 - `mocha_launch/`: launch files the different robots in MOCHA. The launch file
   sets up the `robot_name` argument,
 - `mocha_core/`: MOCHA's main components (source code, config files).
 - `interface_rajant/`: interface for Rajant breadrumb radios

## Docker Configuration (Environment Variables)

When running MOCHA within its Docker container, you can customize its behavior and network configuration using standard Docker environment variables (e.g. `docker run -e WIFI_FALLBACK=false ...`). The container's entrypoint script automatically parses these and passes them to the ROS 2 launch files.

### Networking & Discovery Fallbacks
* **`WIFI_FALLBACK`** *(default: `true`)*: Enables falling back to a WiFi mesh connection when Rajant RSSI drops too low or goes missing.
* **`WIFI_ALWAYS_ON`** *(default: `false`)*: Forces the system to periodically synchronize over WiFi even when the primary Rajant connection is perfectly healthy.
* **`WIFI_BACKUP_PERIOD`** *(default: `10.0`)*: Minimum duration (in seconds) between WiFi backup sync attempts per peer.
* **`RAJANT_TIMEOUT`** *(default: `10.0`)*: Time (in seconds) without receiving a valid RSSI signal before the Rajant connection is considered stale.

### Configuration Paths
MOCHA configurations are injected from the top-level `/home/dtc/config/` directory inside the container. You can override these paths to point to custom `.yaml` configurations mounted via Docker volumes:
* **`ROBOT_CONFIGS`** *(default: `/home/dtc/config/robot_configs.yaml`)*
* **`TOPIC_CONFIGS`** *(default: `/home/dtc/config/topic_configs.yaml`)*
* **`RADIO_CONFIGS`** *(default: `/home/dtc/config/radio_configs.yaml`)*

## Dependencies:

MOCHA requires `rospkg`, `defusedxml`, and `python3-zmq`. You may install these
packages with:

```
sudo apt update
pip3 install rospkg
pip3 install defusedxml
sudo apt install python3-zmq
```

## Contribution - Questions

Please [fill-out an issue](https://github.com/KumarRobotics/MOCHA/issues) if you have any questions.
Do not hesitate to [send your pull request](https://github.com/KumarRobotics/MOCHA/pulls).

## Citation

If you find MOCHA useful, please cite:

```
@INPROCEEDINGS{cladera2024enabling,
  author={Cladera, Fernando and Ravichandran, Zachary and Miller, Ian D. and Ani Hsieh, M. and Taylor, C. J. and Kumar, Vijay},
  booktitle={2024 IEEE International Conference on Robotics and Automation (ICRA)},
  title={{Enabling Large-scale Heterogeneous Collaboration with Opportunistic Communications}},
  year={2024},
  pages={2610-2616},
  doi={10.1109/ICRA57147.2024.10611469}
}
```
