import cv2
import os

# 设置保存图像的目录
output_dir = 'collected_images'
os.makedirs(output_dir, exist_ok=True)

# 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# 设置图像计数器
img_counter = 0

print("Press 'c' to capture image and 'q' to quit.")

while True:
    # 捕获帧
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # 显示帧
    cv2.imshow('Camera', frame)

    # 检测按键
    key = cv2.waitKey(1)

    if key % 256 == ord('c'):
        # 按 'c' 键捕捉图像
        img_name = os.path.join(output_dir, f"image_{img_counter}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"{img_name} saved!")
        img_counter += 1

    elif key % 256 == ord('q'):
        # 按 'q' 键退出
        print("Exiting...")
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
