import cv2
from YOLOv10 import YOLOv10
import time

# 初始化距离值
initial_distance = 120

def test_detect(video_path):
    YOLO_WEIGHTS = "fusion_ais_image/onnx/best.onnx"
    DET_THRES = 0.35
    yolo = YOLOv10(YOLO_WEIGHTS, DET_THRES)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("test_det.mp4", fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    last_time = time.time()  # 记录开始时间
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        

        current_time = time.time()
        elapsed_time = current_time - last_time
        initial_distance = max(initial_distance - int(elapsed_time * 3), 0)  # 计算距离减少
        last_time = current_time

        res = yolo.detect_objects(frame)
        print(res)
        frame = yolo.draw_detections(frame)
        out.write(frame)
        
        cv2.imshow('Processed Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_path = "fusion_ais_image/video/20240726_113533.mp4"
    test_detect(video_path)
