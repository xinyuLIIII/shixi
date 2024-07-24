# 图片检测与AIS数据融合算法

## 依赖

```
#YOLOv8相关依赖
onnxruntime-gpu==1.16.3
numpy==1.26.2
opencv-python==4.8.1

#ffmpeg相关依赖
sudo apt update
sudo apt install nginx
sudo add-apt-repository ppa:nginx/stable
sudo apt install libnginx-mod-rtmp
```

## 代码位置
### 代码位置

位置在[这里](fusion_ais_image)

api接口文档在[文档](fusion_ais_image\WebAPI.md)

通过api接口接收数据的[代码](fusion_ais_image\WebAPI.md)

通过yolov8处理实时传输的视频流[代码](fusion_ais_image\yolo_utils.py)

处理ais经纬度信息变换并计算角度[代码](fusion_ais_image\ship_utils.py)

[主函数代码](fusion_ais_image\total.py)

实现的[前端网页](fusion_ais_image\videoPlayer.html)，需注意要启动http服务，在运行前，终端运行'python -m http.server'，网址为http://<局域网IP地址>:8000/videoPlayer.html
