colcon build --packages-select
source install/setup.bash


ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.2}}"
启动底盘
ros2 run yahboomcar_bringup Ackman_driver_R2
#启动4ROS雷达
ros2 launch ydlidar_ros2_driver ydlidar_launch.py

#启动小车巡线程序 4ROS雷达
ros2 run yahboomcar_linefollow follow_line_4ROS_R2

ros2 topic echo /voltage

ros2 launch my_package gps_imitate_server.launch.py
