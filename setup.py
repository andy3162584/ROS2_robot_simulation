import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'patrol_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # 確保 Launch 檔案被安裝
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.py'))),
        
        # 確保機器人模型 XACRO 被安裝
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.xacro'))),
        
        # 確保 STL 模型被安裝 (不分大小寫)
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.[sS][tT][lL]'))),
        
        # 確保 RViz 設定檔被安裝
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        
        # 【關鍵】確保 World XACRO 檔案被正確搬運
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.xacro'))),
        
        # 確保 Config YAML 檔案被安裝
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andy',
    maintainer_email='andy@todo.todo',
    description='Patrol robot control package using Raspberry Pi 5 and RPLIDAR A1M8',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'patrol_node = patrol_control.patrol_node:main',
        ],
    },
)