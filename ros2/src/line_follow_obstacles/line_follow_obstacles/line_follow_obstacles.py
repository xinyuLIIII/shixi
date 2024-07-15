import rclpy
from rclpy.node import Node
import numpy as np
import cv2
from geometry_msgs.msg import Twist
import tensorflow as tf

class LineFollowerPerceptionNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Set a timer to call `timer_callback` at 10Hz
        self.image_format = "NV12"
        self.dnn_model_path = "src/line_follow_obstacles/model/resnet18_224x224_nv12.bin"

        self.cap = cv2.VideoCapture(0)  # Open the default camera

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open camera")
            rclpy.shutdown()
            return

        self.dnn_model = self.load_dnn_model(self.dnn_model_path)
        if self.dnn_model is None:
            self.get_logger().error("Failed to load DNN model")
            rclpy.shutdown()
            return

    def load_dnn_model(self, model_path):
        try:
            # Load the model using TensorFlow or other appropriate library
            model = tf.keras.models.load_model(model_path)
            return model
        except Exception as e:
            self.get_logger().error(f"Error loading model: {e}")
            return None

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            image_data = self.convert_to_nv12(frame)
            coordinates = self.process_image(image_data)
            twist_msg = self.calculate_twist(coordinates)
            self.publisher_.publish(twist_msg)
        else:
            self.get_logger().error("Failed to capture image from camera")

    def convert_to_nv12(self, frame):
        nv12_image = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
        return nv12_image

    def process_image(self, image_data):
        tensor = self.prepare_nv12_tensor(image_data)
        dnn_output = self.run_dnn_inference(tensor)
        coordinates = self.parse_coordinates(dnn_output)
        return coordinates

    def prepare_nv12_tensor(self, image_data):
        height, width = image_data.shape[:2]
        blob = cv2.dnn.blobFromImage(image_data, scalefactor=1.0, size=(width, height), mean=(0, 0, 0), swapRB=False, crop=False)
        return blob

    def run_dnn_inference(self, blob):
        try:
            self.dnn_model.setInput(blob)
            dnn_output = self.dnn_model.forward()
            return dnn_output
        except Exception as e:
            self.get_logger().error(f"Error during DNN inference: {e}")
            return np.array([[0, 0]])  # Default output in case of error

    def parse_coordinates(self, dnn_output):
        tensor = dnn_output[0]
        x, y = tensor[0], tensor[1]
        result_x = (x * 112 + 112) * 960.0 / 224.0
        result_y = 224 - (y * 112 + 112) + 272 - 112
        return result_x, result_y

    def calculate_twist(self, coordinates):
        twist = Twist()
        x, y = coordinates
        # Generate Twist message based on coordinates
        twist.linear.x = 0.2  # Constant forward speed
        twist.angular.z = -1.0 * (x - 480) / 300.0
        return twist

def main(args=None):
    rclpy.init(args=args)
    node = LineFollowerPerceptionNode('line_follower_perception_node')
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.cap.isOpened():
            node.cap.release()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
