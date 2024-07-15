
## 一、功能包介绍

### 1、livox_ros_driver2



catkin_make -DCATKIN_WHITELIST_PACKAGES="camera_lidar_calibration"

但是如再次使用catkin_make编译所有功能包时会出现仅仅只编译上次设置的单独功能包，如果想要再次使用catkin_make编译所有功能包，需要执行以下命令切换到所有功能包：

catkin_make -DCATKIN_WHITELIST_PACKAGES="calibration_camera_lidar"

sudo apt-get install ros-noetic-serial

sudo apt-get install ros-noetic-jsk-recognition-msgs


rosrun map_server map_saver map:=/projected_map -f /home/jetson/ros1_ws/src/FAST_LIO/PCD/scans

sudo apt install ros-noetic-pointcloud-to-laserscan


rosrun camera_calibration cameracalibrator.py --size 18x16 --square 0.050 image:=/usb_cam/image_raw camera:=/usb_cam

rosrun camera_calibration cameracalibrator.py --size 8x7 --square 0.100 image:=/usb_cam/image_raw camera:=/usb_cam



## 路包数据采集

命令为
```
rosbag record -b 4096 -o test.bag  /livox/imu /livox/lidar /usb_cam/image_raw
```