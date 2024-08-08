import cv2
import os

def capture_frames(video_path, output_folder, prefix, interval=1):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
    frame_interval = int(fps * interval)  # 计算每隔多少帧截取一次
    
    frame_count = 0
    image_count = 0  # 初始命名编号
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 如果到达截取间隔，保存当前帧为图片
        if frame_count % frame_interval == 0:
            image_name = f"{prefix}_{image_count}.jpg"
            image_path = os.path.join(output_folder, image_name)
            cv2.imwrite(image_path, frame)
            print(f"Saved: {image_path}")
            image_count += 1
        
        frame_count += 1
    
    cap.release()
    print("Done capturing frames.")

# 使用示例
video_path = './demo_images/20240801_161034.mp4'  # 视频文件路径
output_folder = './images'        # 截图输出文件夹
prefix = 'test'                      # 文件名前缀

capture_frames(video_path, output_folder, prefix)
