from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Declare arguments
        DeclareLaunchArgument(
            'target_frame', default_value='rslidar_left',
            description='Target frame for point cloud to laser scan conversion'
        ),
        DeclareLaunchArgument(
            'cloud_in_topic', default_value='/rslidar_points_left',
            description='Input point cloud topic'
        ),
        DeclareLaunchArgument(
            'scan_topic', default_value='/left/scan',
            description='Output scan topic'
        ),
        DeclareLaunchArgument(
            'scanner', default_value='scanner',
            description='Namespace for sample topics'
        ),

        # Static Transform Publisher Node
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', '1', 'map', 'cloud']
        ),

        # PointCloud to LaserScan Node
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[
                ('cloud_in', [LaunchConfiguration('cloud_in_topic')]),
                ('scan', [LaunchConfiguration('scan_topic')])
            ],
            parameters=[{
                'target_frame': LaunchConfiguration('target_frame'),
                'transform_tolerance': 0.01,
                'min_height': 0.15,
                'max_height': 1.2,
                'angle_min': -3.14159,  # -M_PI/2
                'angle_max': 3.14159,  # M_PI/2
                'angle_increment': 0.0087,  # M_PI/360.0
                'scan_time': 0.3333,
                'range_min': 0.45,
                'range_max': 50.0,
                'use_inf': True,
                'inf_epsilon': 1.0
            }]
        )
    ])
