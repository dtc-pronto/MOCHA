FROM dtcpronto/ros-jazzy:base

USER dtc
WORKDIR /home/dtc
RUN mkdir -p /home/dtc/ws/src

# Preserve the base image ROS ABI when adding runtime dependencies.
RUN sudo apt update \
    && sudo apt-get install -y --no-upgrade \
    procps python3-pip \
    python3-setuptools \
    python3-zmq \
    default-jre \
    iputils-ping \
    iproute2 \
    python3-lz4 \
    python3-defusedxml \
    python3-serial \
    ros-jazzy-smach \
    ros-jazzy-smach-ros \
    ros-jazzy-nav-msgs \
    ros-jazzy-rclpy \
    ros-jazzy-sensor-msgs \
    ros-jazzy-cv-bridge \
    python3-opencv \
    python3-numpy

RUN pip3 install --user --break-system-packages pyrtcm
RUN pip3 install --user --break-system-packages fastapi 'uvicorn[standard]'
RUN sudo apt update \
    && sudo apt-get install -y --no-upgrade \
    ros-jazzy-vision-msgs
COPY --chown=dtc:dtc . ws/src/MOCHA

RUN /bin/bash -c "\
    source /opt/ros/jazzy/setup.bash && \
    cd /home/dtc/ws && \
    colcon build --symlink-install --cmake-clean-cache"

COPY --chown=dtc:dtc entrypoint.bash /home/dtc/entrypoint.bash
RUN sudo chmod +x /home/dtc/entrypoint.bash

ENTRYPOINT ["/home/dtc/entrypoint.bash"]
