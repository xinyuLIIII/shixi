import cv2
from yolov8.config import YOLO_CLASS_NAMES
from yolov8.YOLOv8 import YOLOv8

def test_detect(img_path):
    YOLOV8_WEIGHTS = "onnx/ship_yolov8.onnx"  # 替换为你的模型路径
    DET_THRES = 0.35
    yolov8 = YOLOv8(YOLOV8_WEIGHTS, DET_THRES)
    
    cv_img = cv2.imread(img_path)
    
    # 检测物体
    boxes, scores, class_ids = yolov8.detect_objects(cv_img)

    # 打印识别到的物体坐标
    for box, score, class_id in zip(boxes, scores, class_ids):
        print(f"Class: {YOLO_CLASS_NAMES[class_id]}, Score: {score:.2f}, Box: {box}")

    # 绘制检测结果
    cv_img = yolov8.draw_detections(cv_img)
    cv2.imwrite("test_det_res.jpg", cv_img)
    
if __name__ == '__main__':
    img_path = "onnx/test_det.png"  # 替换为你的图像路径
    test_detect(img_path)
