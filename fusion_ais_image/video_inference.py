import cv2
from yolo.YOLOv8 import YOLOv8
from cilent import udp_cilent

def test_detect(video_path):
    YOLO_WEIGHTS = "/tmp/ultralytics/best.onnx"
    DET_THRES = 0.38
    yolo = YOLOv8(YOLO_WEIGHTS, DET_THRES)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter("test_det_1.mp4", fourcc, 30.0, (width, height))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            res = yolo.detect_objects(frame)
            print(res)
            udp_cilent(res)
            frame = yolo.draw_detections(frame)
            out.write(frame)
            # 可以注释掉下面的显示，以便服务器或无头环境中运行
            # cv2.imshow('Processed Video', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print("Video processing complete and the file has been saved.")

if __name__ == '__main__':
    video_path = "/tmp/ultralytics/20240802_162509.mp4"
    test_detect(video_path)
