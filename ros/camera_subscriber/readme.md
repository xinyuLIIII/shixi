### 服务器端传输实时推理

设置环境变量
```
chmod +x /home/jetson/camera_subscriber/src/image_processing/src/image_publisher.py

source devel/setup.bash
```
启动节点
```
roscore

rosrun image_processing image_publisher.py
rosrun image_processing image_subscriber.py
```

服务器端

docker中运行
```
docker run -it --gpus all  --network host --name ros_noetic_video_stream -v yolov5:/root yolov5:last

docker start ros_noetic_video_stream
docker exec -it ros_noetic_video_stream bash
```

复制文件到docker
```
docker cp  /tmp/camera_transport/ ros_noetic_video_stream:root/yolo/
```
设置主从机
```
export ROS_MASTER_URI=http://192.168.20.138:11311
export ROS_HOSTNAME=192.168.1.224
```
编译并运行程序
```
cd ~/yolo/camera_transport/
source /opt/ros/noetic/setup.bash
source ~/.bashrc
rm -rf build devel
catkin_make
chmod +x src/image_processing/src/image_subscriber.py
source devel/setup.bash
cd src/image_processing/src/
python image_subscriber.py
```

运行不通时杀死程序
```
ps -ef|grep python

kill -9 <pid>

```
报错 ImportError: /lib/libgdal.so.26: undefined symbol: TIFFReadRGBATileExt, version LIBTIFF_4.0
```
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtiff.so.5
```



