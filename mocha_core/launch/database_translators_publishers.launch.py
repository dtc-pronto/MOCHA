#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """
    Launch database, translator, and topic publisher nodes for MOCHA system
    """

    # Declare launch arguments
    log_level_arg = DeclareLaunchArgument('log_level', default_value='info')
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='charon',
        description='Name of the robot'
    )

    robot_configs_arg = DeclareLaunchArgument(
        'robot_configs',
        default_value=PathJoinSubstitution([
            FindPackageShare('mocha_core'),
            'config', 'robot_configs.yaml'
        ]),
        description='Path to robot configuration file'
    )

    topic_configs_arg = DeclareLaunchArgument(
        'topic_configs',
        default_value=PathJoinSubstitution([
            FindPackageShare('mocha_core'),
            'config', 'topic_configs.yaml'
        ]),
        description='Path to topic configuration file'
    )

    radio_configs_arg = DeclareLaunchArgument(
        'radio_configs',
        default_value=PathJoinSubstitution([
            FindPackageShare('mocha_core'),
            'config', 'radio_configs.yaml'
        ]),
        description='Path to radio configuration file'
    )

    sigterm_timeout_arg = DeclareLaunchArgument(
        'sigterm_timeout', default_value='10',
        description='Modify default SIGTERM timeout to 10 seconds'
    )
    wifi_fallback_enabled_arg = DeclareLaunchArgument(
        'wifi_fallback_enabled', default_value='true',
        description='Use WiFi when Rajant RSSI is weak or missing'
    )
    wifi_backup_always_on_arg = DeclareLaunchArgument(
        'wifi_backup_always_on', default_value='false',
        description='Periodically sync over WiFi even when Rajant is healthy'
    )
    wifi_backup_period_arg = DeclareLaunchArgument(
        'wifi_backup_period', default_value='10.0',
        description='Minimum seconds between WiFi backup sync attempts per peer'
    )
    rajant_signal_timeout_arg = DeclareLaunchArgument(
        'rajant_signal_timeout', default_value='10.0',
        description='Seconds without RSSI before Rajant is considered stale'
    )

    log_level_arg = DeclareLaunchArgument(
        'log_level', default_value=EnvironmentVariable('COMMON_LOG_LEVEL', default_value='info'),
        description='ROS log level for common services'
    )

    respawn_arg = DeclareLaunchArgument(
        'respawn', default_value='false',
        description='Restart nodes after they exit while launch is running'
    )
    respawn_delay_arg = DeclareLaunchArgument(
        'respawn_delay', default_value='5.0',
        description='Seconds to wait before restarting a node'
    )

    return LaunchDescription([
        log_level_arg,
        respawn_arg,
        respawn_delay_arg,
        sigterm_timeout_arg,
        robot_name_arg,
        robot_configs_arg,
        topic_configs_arg,
        radio_configs_arg,
        wifi_fallback_enabled_arg,
        wifi_backup_always_on_arg,
        wifi_backup_period_arg,
        rajant_signal_timeout_arg,
        OpaqueFunction(function=launch_setup)
    ])


def launch_setup(context, *args, **kwargs):
    respawn = LaunchConfiguration('respawn')
    # Jazzy requires a numeric respawn_delay; resolve it at launch execution.
    respawn_delay = float(LaunchConfiguration('respawn_delay').perform(context))
    robot_name = LaunchConfiguration('robot_name')
    robot_configs = LaunchConfiguration('robot_configs')
    topic_configs = LaunchConfiguration('topic_configs')
    radio_configs = LaunchConfiguration('radio_configs')
    wifi_fallback_enabled = LaunchConfiguration('wifi_fallback_enabled')
    wifi_backup_always_on = LaunchConfiguration('wifi_backup_always_on')
    wifi_backup_period = LaunchConfiguration('wifi_backup_period')
    rajant_signal_timeout = LaunchConfiguration('rajant_signal_timeout')

    # Define nodes
    mocha_node = Node(
        package='mocha_core',
        executable='mocha.py',
        name='mocha',
        output='screen',
        arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
        parameters=[{
            'robot_name': robot_name,
            'robot_configs': robot_configs,
            'radio_configs': radio_configs,
            'topic_configs': topic_configs,
            'rssi_threshold': 35,
            'wifi_fallback_enabled': ParameterValue(
                wifi_fallback_enabled, value_type=bool),
            'wifi_backup_always_on': ParameterValue(
                wifi_backup_always_on, value_type=bool),
            'wifi_backup_period': ParameterValue(
                wifi_backup_period, value_type=float),
            'rajant_signal_timeout': ParameterValue(
                rajant_signal_timeout, value_type=float)
        }]
    )

    translator_node = Node(
        package='mocha_core',
        executable='translator.py',
        name='translator',
        output='screen',
        arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
        parameters=[{
            'robot_name': robot_name,
            'robot_configs': robot_configs,
            'topic_configs': topic_configs
        }]
    )

    topic_publisher_node = Node(
        package='mocha_core',
        executable='topic_publisher.py',
        name='topic_publisher',
        output='screen',
        arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')],
        parameters=[{
            'robot_name': robot_name,
            'robot_configs': robot_configs,
            'topic_configs': topic_configs
        }]
    )

    return LaunchDescription([
        log_level_arg,
        sigterm_timeout_arg,
        robot_name_arg,
        robot_configs_arg,
        topic_configs_arg,
        radio_configs_arg,
        wifi_fallback_enabled_arg,
        wifi_backup_always_on_arg,
        wifi_backup_period_arg,
        rajant_signal_timeout_arg,
        mocha_node,
        translator_node,
        topic_publisher_node
    ])
