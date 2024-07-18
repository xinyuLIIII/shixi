# 实习记录

## 1.巡线
 ### 位置
该项目在[linefllow](ros2)

### 完成任务

基于ros2实现小车用摄像头（奥比中光）沿红线循迹 并采用单线激光雷达检测障碍物实现避障功能 具体启动方法见[readme](ros2\README.md)

### 过程
由于这是本次实习第一个项目，主要在于熟悉ros架构和雷达，难度不大，循迹的功能是商家提供的，具体思路是先启动底盘通讯（这也是商家提供的），之后开启摄像头和雷达，最后启动循迹的ros包。

控制底盘运动是通过/cmd_vel这个话题发布订阅信息来实现的，一般控制时只要发布并启动底盘通讯就好，至于怎样运动商家已经写好驱动在这个[位置](ros2\src\yahboomcar_bringup)，以后可以吧这个包直接拿走去用，缺点是总是不稳定有时候通讯不上，可以读取一下电压值看有没有数值来判断，若没有就重启(目前没有在其他车上试验过，不确定是否有适用性，不过可以拿来改)。

#### 遇到的问题及解决办法

1. 这个项目的搭建是通过商家提供的docker环境中一点点拉取的，在这个过程中需要根据拉取的包的报错安装依赖，这个看报错提示就好

2. 雷达、相机的驱动安装需要知道型号，然后上网搜索安装办法，以后有相关的工作可以参考，雷达选型选择揽沃或者速腾好一点，相机选用英伟达D45。

3. 相机启动时可能打不开，这是因为在汽车启动时，会弹出一个报告启动状态的框占用了端口，给他杀死就好了

## 2.基于YOLOV5和ROS实现在小车传输图像在服务器上推理并推流到网页
### 位置
汽车上的代码在[image_subscriber](ros\camera_subscriber)

服务器端代码在[image_transport](ros\camera_transport)
### 完成任务
通过小车的摄像头拍摄图片，并配置ros的主从机实现图片实时被服务器订阅，服务器订阅后通过yolov5进行实时推理，并将推理结果采用http的方式推流到网页实现实时显示。

### 过程
首先是实现小车上通过摄像头拍摄并发布，这里比较简单代码在[ros\camera_subscriber\src\image_processing\src\image_publisher.py](ros\camera_subscriber\src\image_processing\src\image_publisher.py)

之后要做的是配置主从机，我是将小车配置为主机，要做的是修改~/.bashrc文件,命令为
```
nano ~/.bashrc
```
最后两行添加内容
```
export ROS_MASTER_URI=http://小车ip:11311
export ROS_HOSTNAME=小车IP
<!-- PS：
export ROS_MASTER_URI=http://192.168.20.138:11311
export ROS_HOSTNAME=192.168.20.138 -->
```

配置从机需要在服务器上执行命令：
```
export ROS_MASTER_URI=http://服务器IP:11311
export ROS_HOSTNAME=服务器IP

<!-- ps:
export ROS_MASTER_URI=http://192.168.20.138:11311
export ROS_HOSTNAME=192.168.1.224 -->
```

在这个过程中，由于环境限制，拉取了docker，一般来说具体拉取就是一行命令，但是需要在dockerhub里找到自己需要的docker，也可以问gpt。但在拉取容器到服务器这个过程中遇到了问题，这是由于国内网络限制的原因无法拉取docker，解决办法见[解决办法](#遇到的问题及解决办法-1)中的第一点

在拉取的docker中已经配置好了yolo的环境，接下来要实现的是通过ros订阅到图像，这里遇到的问题是无法订阅到，[原因和解决办法在第二点](#遇到的问题及解决办法-1)，这部分代码在[image_subscriber.py](ros\camera_transport\src\image_processing\src\image_subscriber.py)

在订阅图像后需要将图像进行推理，然后将推理后结果上传到网页，网址为http://服务器IP:8080/video代码也在[image_subscriber.py](ros\camera_transport\src\image_processing\src\image_subscriber.py)，值得一提的是，这里有很多代码都是自己写或者添加的，可以拿来参考或以后直接调用，实现的功能有：
1. delete_images：按照文件名排序删图片
2. RemoveDir：如果文件夹不存在就创建，如果文件存在就清空


需要注意的点也在[原因和解决办法](#遇到的问题及解决办法-1)。





### 遇到的问题及解决办法
1. 对于无法拉取docker，一般来说换源即可，实在不行，可以在windows下先翻墙下载，然后通过命令将其打包压缩，之后再将打包好的文件上传到服务器，之后在接下即可，[具体可见这里](https://blog.csdn.net/sunmingyang1987/article/details/104555190)
之后即可正常启动进入，步骤见[readme](ros\camera_subscriber\readme.md)
。在进入容器之前（或进入容器后另起终端）可以需要将要运行的代码复制进入容器代码也在[readme](ros\camera_subscriber\readme.md)
2. 一般来说对于无法顺利订阅，原因都是主从机没有配置好，请检查IP地址是否正确，若正确且是用服务器订阅，需要开通端口11311以及udp传输的权限，联系老师或者运维即可
3. 这段代码是基于[detect.py](ros\camera_transport\src\image_processing\src\detect.py)改的，但是没有改完，只实现了图片的实时推理，另外还修改了函数LoadImages,他在[dataloaders.py](ros\camera_transport\src\image_processing\src\utils\dataloaders.py) 中
4. 对于图像的推理重点要关注的变量是run函数中的im0，它是推理后的图片，在对推理的后续有任何操作都可以直接调用这个变量，对于推理的具体细节并不用过多的去关注。
5. 采用了HTTP的方式将处理后的im0信息传输到网页，之前这里卡住好久，原因是之前对于ros系统、推理以及网页显示，为了确保能够不被卡住采用了多线程的操作，但是这样同一变量无法做到在不同线程同时更新，依然不是实时的。后来考虑加线程锁，但是这种方式更新的很慢，在网页上显示的仍然不实时。所以最后将ros订阅图片和推理放在一个类中，这样使得多线程变为双线程，有采用队列的方式将同一变量实现不同线程间能够公用。

## 基于多线雷达的slam建图与导航

### 代码位置

在[ros1_ws](ros\ros1_ws)下


由于这个工程不是我做的，只是接手过来，所以原理并不太懂，只知道怎么运行和大概原理，具体见[说明文档](ros\ros1_ws\说明文档补充.md)

## AIS信息与图像信息匹配

这个工程是现在在做的，所以可以每天记录，更加详细一点

### 代码位置

位置在[这里](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755)

api接口文档在[文档](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\WebAPI.md)

通过api接口接收数据的[代码](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\WebAPI.md)

通过yolov8处理实时传输的视频流[代码](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\yolo_utils.py)

处理ais经纬度信息变换并计算角度[代码](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\ship_utils.py)

[主函数代码](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\total.py)

### 完成任务

通过采集船只自身摄像头和ais信息和周围ais信息，将摄像头内识别到的船匹配它的ais信息

想提一下的是，在这个过程中尝试了用深度估计的办法来测距，代码为[monodepth2](monodepth2\AIS_MONO.py),这里存在的问题是纹理不是很明显，远处的船和背景融为一体，而且在有几条船的时候很难区分出距离远近，深度估计现在看来可以用在近距离或纹理较为明显的情况下测距。另一种深度估计为depth_anything，但这种对于显卡要求较高，需要四张3090/3080所以并未尝试，而且从[官网](https://github.com/LiheYoung/Depth-Anything)看起来好于monodepth但仍不满足使用场景。

### 具体实现功能
1. 根据图片用yolov8实现推理识别船舶，环境为虚拟机环境labelimg_e。
2. 用python自带的库根据船只自身和目标船只的经纬度坐标以及船只自身朝向计算两船之间夹角和距离
3. 根据yolo所识别出的结果计算船只到摄像头的夹角（即图片下边缘的中心点为原点下边缘为x轴，垂线为y轴建立坐标系，计算船只与y轴的夹角）
4. 匹配ais与图像计算出的角度
### 每日记录
#### 7.9
摆
#### 7.10
摆
#### 7.11
摆
#### 7.12
摆了一周，目前存在问题为由于摄像头的畸变问题以及摄像头的水平朝向与ais记录的船只朝向不一定相同的问题导致ais计算的角度与通过图像计算的角度差别很大，暂无解决方法，需要真实数据调试后才知道。另外，真实数据中船舶的ais信息不一定有而且也不一定准确。

#### 7.15
拿到了ais信息和视频的接口文档，写了接口调用同时做了测试，但发现视频是wss形式，没办法直接被cv处理，研究了半天也没找到方法

#### 7.16
找到了http协议的视频，用它做了测试，完成了用yolov8做视频的实时推理。能够和之前的代码融合起来，在计算出来角度并显示出来。通过调用ais接口得到附件船舶ais信息，测算出了每艘船距离该船只的角度与距离。

已经做完了融合，并且做了模块化处理。

#### 7.17
蹲一上午数据，终于有了，位置在[autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\video](autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755\video)



