### Introduction
This project is an automated patrol robot simulation system built on the ROS2 Jazzy framework. It aims to simulate real-world scenarios for Simultaneous Localization and Mapping (SLAM) and autonomous navigation tasks.  

本專案是基於 ROS2 Jazzy 框架建構的自動化巡邏機器人模擬系統。目的在模擬現實世界中同步定位與建圖（SLAM）和自主導航任務。
  
  
### Development Environment
* OS : ubuntu 24.04 LTS  
* ROS2 version : ROS2 Jazzy  
* Simulation software : Gazebo / RVIZ2  
* Language : python / xml (xacro)  

### Project structure 
* config
  * 
* launch
  * robot_sim.launch.py - 
* meshes - 3D geometry of robot appearance
* rviz - rviz configuration file
* urdf 
  * patrol_robot.xacro - The URDF file mainly defines the robot’s structure, joint configuration, and appearance model.
* worlds