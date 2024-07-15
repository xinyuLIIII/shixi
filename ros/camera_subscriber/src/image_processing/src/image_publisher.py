#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main():
    rospy.init_node('camera_publisher', anonymous=True)
    image_pub = rospy.Publisher("/camera/image", Image, queue_size=10)
    bridge = CvBridge()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        rospy.logerr("Cannot open camera")
        return

    rate = rospy.Rate(5)  

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            rospy.logerr("Failed to capture image")
            break

        try:
            image_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
            image_pub.publish(image_msg)
        except CvBridgeError as e:
            rospy.logerr("CvBridge Error: {0}".format(e))

        rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
