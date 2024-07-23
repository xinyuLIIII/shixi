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
api接口文档在[文档](WebAPI.md)

通过api接口接收数据的[代码](API.py)

通过yolov8处理实时传输的视频流[代码](yolo_utils.py)

处理ais经纬度信息变换并计算角度[代码](ship_utils.py)

[主函数代码](total.py)

## rtmp
IN /etc/nginx/nginx.conf

rtmp {
    server {
        listen 1935; # RTMP 监听端口
        chunk_size 4096;

        application live { # 'live' 是应用名，可以自定义
            live on;
            record off; # 关闭录制
        }
    }
}

REBOOT

sudo systemctl restart nginx
