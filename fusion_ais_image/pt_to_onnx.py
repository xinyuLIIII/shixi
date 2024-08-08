from ultralytics import YOLO
 
# 加载模型
model = YOLO('yolov8x.pt')  # 加载官方模型
model = YOLO('/tmp/ultralytics/runs/detect/train5/weights/best.pt')  # 加载自定义训练模型
 
# 导出模型
model.export(format='onnx')