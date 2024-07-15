#!/usr/bin/env python

import rospy
import threading
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import time

def image_publisher():
    # 初始化ROS节点
    rospy.init_node('image_publisher', anonymous=True)
    image_dir = "runs/detect/exp4" 
    # 创建发布者
    image_pub = rospy.Publisher("/camera/yolo", Image, queue_size=10)

    # time.sleep(0.5)
    # 创建cv_bridge实例
    bridge = CvBridge()

    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        for image_file in os.listdir(image_dir):
            if image_file.endswith(".jpg"):  # 假设只处理.jpg格式的文件
                image_path = os.path.join(image_dir, image_file)
                try:
                    # 读取图片文件
                    cv_image = cv2.imread(image_path)
                    # 将OpenCV图像转换为ROS消息
                    ros_image = bridge.cv2_to_imgmsg(cv_image, "bgr8")
                    # rospy.loginfo(ros_image)
                    # 发布ROS消息
                    image_pub.publish(ros_image)
                    rospy.loginfo(f"发布图片 {image_path}")
                    rate.sleep()
                except CvBridgeError as e:
                    rospy.logerr("CvBridge 错误: {0}".format(e))
                except FileNotFoundError:
                    rospy.logerr(f"文件未找到: {image_path}")
                except Exception as e:
                    rospy.logerr(f"处理图片时出错: {e}")

    

if __name__ == '__main__':
    try:
        image_publisher()
        # rospy.spin()
    except rospy.ROSInterruptException:
        pass
