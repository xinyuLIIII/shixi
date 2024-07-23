import numpy as np

from yolo.utils import xywh2xyxy, draw_detections, multiclass_nms
from yolo.model_onnx import ModelOnnx

class YOLOv8(ModelOnnx):


    def process_output(self, output, conf_thres=None):
        if conf_thres is None:
            conf_thres = self.conf_threshold

        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > conf_thres, :]
        scores = scores[scores > conf_thres]

        if len(scores) == 0:
            return [], [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        xywh_boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(xywh_boxes)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        return boxes[indices], scores[indices], class_ids[indices], xywh_boxes[indices]

