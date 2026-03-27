import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory('patrol_control')

    # ==============================
    # 1. 解析 Robot URDF (xacro)
    # ==============================
    robot_xacro = os.path.join(pkg_share, 'urdf', 'patrol_robot.xacro')
    robot_description = xacro.process_file(robot_xacro).toxml()
    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')

    # ==============================
    # 2. 解析 World (xacro -> sdf)
    # ==============================
    world_xacro_path = os.path.join(pkg_share, 'worlds', 'world.xacro')
    world_description = xacro.process_file(world_xacro_path).toxml()
    
    world_temp_path = "/tmp/patrol_world.sdf"
    with open(world_temp_path, "w") as f:
        f.write(world_description)

    # ==============================
    # 3. 檔案路徑與環境變數
    # ==============================
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'patrol_robot.rviz')

    resource_path = [
        os.path.join(pkg_share, 'models'),
        os.path.join(pkg_share, 'worlds'),
        os.path.join(pkg_share, '..')
    ]

    env = {
        'LIBGL_ALWAYS_SOFTWARE': '1',
        'GZ_SIM_RESOURCE_PATH': ':'.join(resource_path),
        'GZ_SIM_SYSTEM_PLUGIN_PATH': os.environ.get('GZ_SIM_SYSTEM_PLUGIN_PATH', ''),
        'OGRE_RTT_MODE': 'CopyBack',
        'QT_QPA_PLATFORM': 'xcb'
    }

    # ==============================
    # 4. 節點定義
    # ==============================
    
    # Gazebo 模擬器
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_temp_path, '-v', '4'],
        output='screen',
        additional_env=env
    )

    # Robot State Publisher
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # ROS <-> Gazebo Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        parameters=[{
            'use_sim_time': True,
            'qos_overrides./scan.reliability': 'reliable',
            'qos_overrides./imu/data.reliability': 'best_effort',
        }],
        output='screen'
    )

    # Spawn Robot (保留 3 秒延遲確保 Gazebo 已載入)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'patrol_robot',
            '-topic', 'robot_description',
            '-x', '0', '-y', '0', '-z', '0.2'
        ],
        output='screen'
    )

    spawn_delay = TimerAction(
        period=3.0,
        actions=[spawn_robot]
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path, {'use_sim_time': True}]
    )

    # ==============================
    # 強制發布 base_link -> chassis
    static_tf_chassis = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.22', '0', '0', '0', 'base_link', 'chassis']
    )

    # 強制發布 chassis -> laser_frame
    static_tf_laser = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.1', '0', '0', '0', 'chassis', 'laser_frame']
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        bridge,
        spawn_delay,
        rviz,
        robot_localization_node
    ])