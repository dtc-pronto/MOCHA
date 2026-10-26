FROM dtcpronto/ros-jazzy:base

USER dtc
WORKDIR /home/dtc
RUN mkdir -p /home/dtc/ws/src

RUN sudo apt update && sudo apt install -y \
    default-jre-headless \
    python3-defusedxml \
    python3-lz4 \
    python3-pip \
    python3-rospkg \
    python3-zmq \
    python3-yaml \
    ros-jazzy-ament-cmake-python \
    ros-jazzy-geometry-msgs \
    ros-jazzy-rosidl-default-generators \
    ros-jazzy-sensor-msgs \
    ros-jazzy-std-msgs \
    ros-jazzy-vision-msgs

COPY --chown=dtc:dtc . ws/src/MOCHA

RUN /bin/bash -c "\
    source /opt/ros/jazzy/setup.bash && \
    cd /home/dtc/ws && \
    colcon build --symlink-install --cmake-clean-cache"

COPY --chown=dtc:dtc entrypoint.bash /home/dtc/entrypoint.bash
RUN sudo chmod +x /home/dtc/entrypoint.bash

ENTRYPOINT ["/home/dtc/entrypoint.bash"]
