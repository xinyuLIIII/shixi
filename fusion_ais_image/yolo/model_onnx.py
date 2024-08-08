from abc import ABC, abstractmethod
import time
import cv2
import numpy as np
import onnxruntime

from yolo.utils import draw_detections

class ModelOnnx(ABC):
    
    def __init__(self, path, conf_thres=0.5, iou_thres=0.45):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        # self.distance = 120
        # self.last_time = time.time()  # 记录初始化时间
        # self.accumulated_time = 0 
        # Initialize model
        self.initialize_model(path)

    def __call__(self, image):
        return self.detect_objects(image)

    def initialize_model(self, path):
        self.session = onnxruntime.InferenceSession(path,
                                                    providers=onnxruntime.get_available_providers())
        # Get model info
        self.get_input_details()
        self.get_output_details()

    # def update_distance(self):
    #     current_time = time.time()
    #     elapsed_time = current_time - self.last_time
    #     self.accumulated_time += elapsed_time
        
    #     if self.accumulated_time >= 10:  # 每累积10秒
    #         self.distance = max(self.distance - 1, 0)  # 减少1米
    #         self.accumulated_time = 0  # 重置累积时间
        
    #     self.last_time = current_time  # 更新时间


    def detect_objects(self, image):
        input_tensor = self.prepare_input(image)

        # Perform inference on the image
        outputs = self.inference(input_tensor)

        self.boxes, self.scores, self.class_ids, self.xywh_boxes = self.process_output(outputs)

        return self.boxes, self.scores, self.class_ids

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Unable to open video.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # self.update_distance()  # 更新距离

            # Detect objects in the frame
            _, _, _ = self.detect_objects(frame)

            # Draw detections on the frame
            detected_frame = self.draw_detections(frame)
            # Display the frame with detections
            cv2.imshow('YOLOv8 Detection', detected_frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]

        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)

        return input_tensor


    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(self.output_names, {self.input_names[0]: input_tensor})

        print(f"Inference time: {(time.perf_counter() - start)*1000:.2f} ms")
        return outputs

    @abstractmethod
    def process_output(self, output, conf_thres=None):
        pass
    
    def rescale_boxes(self, boxes):

        # Rescale boxes to original image dimensions
        ratio_w = self.img_width / self.input_width
        ratio_h = self.img_height / self.input_height
        boxes *= np.array([ratio_w, ratio_h, ratio_w, ratio_h])
        return boxes
    
    
    def draw_detections(self, image, mask_alpha=0.4):

        return draw_detections(image, self.boxes, self.scores,
                               self.class_ids, mask_alpha)


    # def draw_detections(self, image):
    #     # global initial_distance
    #     # 寻找最大的检测框
    #     largest_area = 0
    #     largest_box = None
    #     self.update_distance()  # 更新距离
    #     for box in self.boxes:
    #         x1, y1, x2, y2 = map(int, box)
    #         area = (x2 - x1) * (y2 - y1)
    #         if area > largest_area:
    #             largest_area = area
    #             largest_box = (x1, y1, x2, y2)
        
    #     # 只绘制最大的框，不显示任何文本
    #     if largest_box and largest_area >3000:
    #         x1, y1, x2, y2 = largest_box
    #         cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 使用红色绘制矩形框  
    #         label = f"distance: {self.distance}m"
    #         cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #         #cv2.putText(image, f"Distance: {self.distance}m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #     return image

    def get_input_details(self):
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]