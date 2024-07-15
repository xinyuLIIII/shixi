设置环境变量
```
chmod +x /home/jetson/catkin_ws/src/my_astra_camera/src/image_publisher.py

source devel/setup.bash
```
启动节点
```
roscore

rosrun my_astra_camera image_publisher.py
```

服务器端

docker中运行
```
docker run -it --gpus all  --network host --name ros_noetic_video_stream -v yolov5:/root -v  my_ros_yolov5:latest
docker run -it --gpus all --network host --name ros_noetic_video_stream -v /tmp/camera_subscriber/:/root/ros_video -v yolov5:/app/yolov5 my_ros_yolov5:latest


docker start ros_noetic_video_stream
docker exec -it ros_noetic_video_stream bash
```
通过 docker ps-a 查看ros_noetic_video_stream ID

启动docker
```
export ROS_MASTER_URI=http://192.168.20.138:11311
export ROS_HOSTNAME=192.168.1.224
cd /tmp/ros_video/
source /opt/ros/noetic/setup.bash
source ~/.bashrc
rm -rf build devel
catkin_make
chmod +x src/image_processing/src/image_subscriber.py
source devel/setup.bash
cd src/image_processing/src/
python3 image_subscriber.py
```



