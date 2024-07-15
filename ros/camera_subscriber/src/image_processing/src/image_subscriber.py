#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os

class ImageSubscriber:

    def __init__(self):
        # 初始化节点
        rospy.init_node('image_subscriber', anonymous=True)

        # 创建cv_bridge实例
        self.bridge = CvBridge()

        # 订阅图像话题
        self.image_sub = rospy.Subscriber("/camera/yolo", Image, self.image_callback)

        # # 图像保存路径
        # self.image_save_path = "saved_images"
        # if not os.path.exists(self.image_save_path):
        #     os.makedirs(self.image_save_path)
        
        # # 图像计数器
        # self.image_counter = 0

    def image_callback(self, data):
        try:
            # 将ROS图像消息转换为OpenCV图像
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))
            return

        # 显示图像
        cv2.imshow('Received Image', cv_image)
        cv2.waitKey(1)  # 等待1毫秒，这样可以给系统处理其他事件的时间，例如按键事件

        # # 将图像保存为JPEG格式
        # image_filename = os.path.join(self.image_save_path, f"image_{self.image_counter:04d}.jpg")
        # cv2.imwrite(image_filename, cv_image)
        # rospy.loginfo(f"Saved image {image_filename}")
        # self.image_counter += 1

if __name__ == '__main__':
    try:
        ImageSubscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
