# Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    this_package = FindPackageShare('champ_config')

    bringup_launch_path = PathJoinSubstitution(
        [FindPackageShare('champ_bringup'), 'launch', 'bringup.launch.py']
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            name='robot_name', 
            default_value='',
            description='Set robot name for multi robot'
        ),

        DeclareLaunchArgument(
            name='sim', 
            default_value='false',
            description='Enable use_sime_time to true'
        ),

        DeclareLaunchArgument(
            name='rviz', 
            default_value='false',
            description='Run rviz'
        ),

        DeclareLaunchArgument(
            name="rviz_path",
            default_value=PathJoinSubstitution(
                [FindPackageShare('champ_description'), 'rviz', 'urdf_viewer.rviz']
                ),
            description="Absolute path to rviz file",
        ),
    
        DeclareLaunchArgument(
            name='hardware_connected', 
            default_value='false',
            description='Set to true if connected to a physical robot'
        ),

        DeclareLaunchArgument(
            name="description_path",
            default_value=PathJoinSubstitution(
                [FindPackageShare('champ_description'), 'urdf', 'champ.urdf.xacro']
                ),
            description="Absolute path to robot urdf file",
        ),

        DeclareLaunchArgument(
            name="joints_map_path",
            default_value=PathJoinSubstitution(
                [FindPackageShare('champ_config'), 'config/joints', 'joints.yaml']
                ),
            description="Absolute path to robot joints config file",
        ),

        DeclareLaunchArgument(
            name="links_map_path",
            default_value=PathJoinSubstitution(
                [FindPackageShare('champ_config'), 'config/links', 'links.yaml']
                ),
            description="Absolute path to robot links config file",
        ),

        DeclareLaunchArgument(
            name="gait_config_path",
            default_value=PathJoinSubstitution(
                [FindPackageShare('champ_config'), 'config/gait', 'gait.yaml']
                ),
            description="Absolute path to robot gait config file",
        ),
    
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(bringup_launch_path),
            launch_arguments={
                "use_sim_time": LaunchConfiguration("sim"),
                "robot_name": LaunchConfiguration("robot_name"),
                "gazebo": LaunchConfiguration("sim"),
                "rviz": LaunchConfiguration("rviz"),
                "hardware_connected": LaunchConfiguration("hardware_connected"),
                "publish_foot_contacts": "true",
                "close_loop_odom": "true",
                "joint_controller_topic": "joint_group_effort_controller/joint_trajectory",
                "description_path": LaunchConfiguration("description_path"),
                "joints_map_path": LaunchConfiguration("joints_map_path"),
                "links_map_path": LaunchConfiguration("links_map_path"),
                "gait_config_path": LaunchConfiguration("gait_config_path")
            }.items(),
        ),
        
        Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', LaunchConfiguration("rviz_path")],
            condition=IfCondition(LaunchConfiguration("rviz"))
        )
    ])
