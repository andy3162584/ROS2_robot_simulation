## Introduction
This project is an automated patrol robot simulation system built on the ROS2 Jazzy framework. It aims to simulate real-world scenarios for Simultaneous Localization and Mapping (SLAM) and autonomous navigation tasks.  

本專案是基於 ROS2 Jazzy 框架建構的自動化巡邏機器人模擬系統。目的在模擬現實世界中同步定位與建圖（SLAM）和自主導航任務。
  
  
## Development Environment
* OS : ubuntu 24.04 LTS  
* ROS2 version : ROS2 Jazzy  
* Simulation software : Gazebo / RVIZ2  
* Language : python / xml (xacro)  

## Project structure 
* config
  * bridge_config.yaml - Define the bridging parameters between ROS 2 and Gazebo
  * mapper_params_online_async.yaml - SLAM Toolbox core parameter file
* launch
  * robot_sim.launch.py - Launch Gazebo and import maps and bots, enable RVIZ, and establish communication between the bot and Gazebo.
* meshes - 3D geometry of robot appearance
* rviz - rviz configuration file
* urdf 
  * patrol_robot.xacro - This file mainly defines the robot’s structure, joint configuration, and appearance model
* worlds
  * world.xacro - Define the scenario of the simulation environment
* setup.py - The project's installation script ensures that launch can find the file.
   
   
