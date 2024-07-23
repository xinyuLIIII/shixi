import numpy as np

from yolo.utils import xywh2xyxy, draw_detections, multiclass_nms
from yolo.model_onnx import ModelOnnx

class YOLOv10(ModelOnnx):
    
    
    def process_output(self, output, conf_thres=None):
        if conf_thres is None:
            conf_thres = self.conf_threshold

        predictions = np.squeeze(output[0])
        print(f"predictions.shape: {predictions.shape}")

        # Filter out object confidence scores below threshold
        scores = predictions[:, 4]
        predictions = predictions[scores > conf_thres, :]
        scores = scores[scores > conf_thres]
        print(f"scores: {scores.shape} {scores}")

        if len(scores) == 0:
            return [], [], [], []

        # Get the class with the highest confidence
        class_ids = predictions[:, 5].astype(int)

        # Extract boxes from predictions
        boxes = predictions[:, :4]
        print(f'boxes: {boxes}')
        
        xywh_boxes = None

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        return boxes[indices], scores[indices], class_ids[indices], xywh_boxes
    