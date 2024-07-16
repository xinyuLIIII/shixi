import pandas as pd
from ship_utils import calculate_relative_positions
from API import ShipServiceAPI
from yolo_utils import detect_video_stream

def main():
    camera_para = [113.232715, 22.7410167, 17]  # 相机参数 (经度, 纬度, 水平朝向)
    api = ShipServiceAPI()
    ships_data = api.get_nearby_ships("413837924")  # 假设这里返回的ships_data包含mmsi字段

    if isinstance(ships_data, list):  # 确保API调用成功
        # 将数据转换为DataFrame
        target_points = pd.DataFrame({
            'lon': [ship['longitude'] for ship in ships_data],
            'lat': [ship['latitude'] for ship in ships_data],
            'mmsi': [ship['maritimeMobileServiceIdentity'] for ship in ships_data]
        })
        results = calculate_relative_positions(target_points, camera_para)
        angle_mmsi_mapping = {float(row['angle_with_x_axis']): row['mmsi'] for index, row in results.iterrows()}
    else:
        print("API call failed:", ships_data)
        return

    YOLOV8_WEIGHTS = "autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755/onnx/ship_yolov8.onnx"  # 替换为你的模型路径
    DET_THRES = 0.35
    
    # 获取视频流URL
    device_no = "hw_mera0808_1"
    url = api.get_camera_video_stream(device_no)
    
    if url:
        # 进行检测，传递角度与MMSI映射
        detect_video_stream(url, YOLOV8_WEIGHTS, DET_THRES, angle_mmsi_mapping,"autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755/video/video_output.avi")
    else:
        print("Failed to get video stream URL.")

if __name__ == "__main__":
    main()
