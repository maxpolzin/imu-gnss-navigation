# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    pkg_ros_gz_sim_demos = get_package_share_directory('ros_gz_sim_demos')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': '-v 4 -r /home/max/gz_ws/src/ros_gz/ros_gz_sim_demos/worlds/diff_drive.sdf'
        }.items(),
    )

    # RViz
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(pkg_ros_gz_sim_demos, 'rviz', 'diff_drive.rviz')],
       condition=IfCondition(LaunchConfiguration('rviz'))
    )

    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                   '/model/vehicle_blue/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                   '/gps/fix@sensor_msgs/msg/NavSatFix@gz.msgs.NavSat', 
                   '/imu@sensor_msgs/msg/Imu@gz.msgs.IMU'],
        parameters=[{'qos_overrides./model/vehicle_blue.subscriber.reliability': 'reliable'}],
        output='screen'
    )


    # sdf_file = os.path.join(pkg_ros_gz_sim_demos, 'models', 'vehicle', 'model.sdf')

    # with open(sdf_file, 'r') as infp:
    #     robot_desc = infp.read()

    # robot_state_publisher = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     name='robot_state_publisher',
    #     output='both',
    #     parameters=[
    #         {'use_sim_time': True},
    #         {'robot_description': robot_desc},
    #     ]
    # )

    return LaunchDescription([
        gz_sim,
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz.'),
        bridge,
        rviz,
        # robot_state_publisher
    ])
