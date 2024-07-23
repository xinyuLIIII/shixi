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


    def get_input_details(self):
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]