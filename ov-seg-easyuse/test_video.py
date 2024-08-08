import cv2
from ov_seg_easyuse import OvSegEasyuse
from PIL import Image

# 初始化模型
class_definition = { 'boat': [0,0,255]}
ose = OvSegEasyuse(class_definition)

def process_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, codec, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # 处理每一帧并返回处理结果
            vis_image = ose.inference(frame)  # 使用新的推理方法
            if hasattr(vis_image, 'get_image'):  # 检查对象是否有 get_image 方法
                processed_frame = vis_image.get_image()  # 获取 numpy 数组
            else:
                processed_frame = vis_image  # 或其他适当的错误处理

            out.write(processed_frame)
        else:
            break

    cap.release()
    out.release()

# 调用函数
input_video_path = './demo_images/20240801_161034.mp4'
output_video_path = 'path_to_output_video.mp4'
process_video(input_video_path, output_video_path)
print ("finish")
