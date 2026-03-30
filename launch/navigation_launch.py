import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. 獲取路徑
    pkg_dir = get_package_share_directory('patrol_control')
    
    # 2. 定義參數
    use_sim_time = LaunchConfiguration('use_sim_time')
    map_yaml_file = LaunchConfiguration('map')
    # 這裡確保如果沒傳入 params_file，會去讀取你的 config 資料夾
    params_file = LaunchConfiguration('params_file', default=os.path.join(pkg_dir, 'config', 'nav2_params.yaml'))
    
    # 3. 定義各個 Nav2 節點
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[params_file] # 只傳這個，yaml_filename 寫在 nav2_params.yaml 裡
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[params_file]
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[params_file]
    )

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[params_file]
    )

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[params_file]
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[params_file]
    )
    
    # 4. 生命週期管理器 (Lifecycle Manager) - 這是 Nav2 正常啟動的關鍵
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_service',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': [
                'map_server', 
                'amcl', 
                'planner_server', 
                'controller_server', 
                'behavior_server', 
                'bt_navigator'
            ]
        }]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='True'),
        DeclareLaunchArgument('map', default_value=os.path.join(pkg_dir, 'maps', 'my_patrol_map.yaml')),
        DeclareLaunchArgument('params_file', default_value=os.path.join(pkg_dir, 'config', 'nav2_params.yaml')),
        
        map_server,
        amcl,
        planner_server,
        controller_server,
        behavior_server,
        bt_navigator,
        lifecycle_manager
    ])