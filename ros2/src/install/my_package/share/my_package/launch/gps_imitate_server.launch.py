import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='my_package',
            executable='gps_imitate_server',
            output='screen',
            name='gps_imitate_server'
        )
    ])
