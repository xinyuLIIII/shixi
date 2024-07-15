import cv2
import numpy as np
import math

def find_red_boxes(image, min_area=1000):
    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the red color range
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    mask = mask1 + mask2
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area >= min_area:
            boxes.append((x, y, w, h))
    
    return boxes

def calculate_angle(center_point, bottom_center):
    dx = center_point[0] - bottom_center[0]
    dy = bottom_center[1] - center_point[1]
    
    # Angle with the vertical line
    angle = math.degrees(math.atan2(dx, dy))
    return angle

def draw_boxes_with_angles(image, boxes, angles):
    for i, box in enumerate(boxes):
        x, y, w, h = box
        angle = angles[i]
        
        # Draw the rectangle
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw the angle text
        text = f"{angle:.2f} degrees"
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image

def main(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to open.")
    
    height, width, _ = image.shape
    
    # Find red boxes with minimum area filter
    boxes = find_red_boxes(image, min_area=1000)
    
    # Calculate bottom center point
    bottom_center = (width // 2, height)
    
    # Calculate angles for each box
    angles = []
    for box in boxes:
        x, y, w, h = box
        left_center = (x, y + h // 2)
        right_center = (x + w, y + h // 2)
        
        # Calculate distances to the vertical line
        left_distance = abs(left_center[0] - bottom_center[0])
        right_distance = abs(right_center[0] - bottom_center[0])
        
        # Debugging information
        print(f"Box: {box}")
        print(f"Left center: {left_center}, Right center: {right_center}")
        print(f"Left distance: {left_distance}, Right distance: {right_distance}")
        
        # Choose the closer point to the vertical line
        if left_distance < right_distance:
            center_point = left_center
        else:
            center_point = right_center
        
        angle = calculate_angle(center_point, bottom_center)
        angles.append(angle)
    
    # Draw boxes and angles on the image
    image_with_angles = draw_boxes_with_angles(image, boxes, angles)
    
    # Save or display the image
    output_path = "output_image_with_angles.jpg"
    cv2.imwrite(output_path, image_with_angles)
    cv2.imshow("Image with Angles", image_with_angles)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = "2024-07-05 17-49-37.jpg"  # Update with the path to your image
    try:
        main(image_path)
    except Exception as e:
        print(f"An error occurred: {e}")
