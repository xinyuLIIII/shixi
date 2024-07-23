import subprocess
import cv2
import pandas as pd
from ship_utils import calculate_relative_positions
from API import ShipServiceAPI
from yolo_utils import initialize_video_stream, process_frame, display_and_save_frame



def stream_video_to_rtmp(output_url, cap, yolov8, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles):
    # 定义ffmpeg命令，将输出推送到RTMP服务器
    command = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-f', 'rawvideo',  # 输入格式为原始视频
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',  # 输入像素格式
        '-s', '{}x{}'.format(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),  # 输入视频大小
        '-r', '0.1',  # 输入帧率
        '-i', '-',  # 从stdin读取输入
        '-c:v', 'libx264',  # 输出视频编码
        '-pix_fmt', 'yuv420p',  # 输出像素格式
        '-preset', 'ultrafast',  # 编码速度和质量的平衡
        '-f', 'flv',  # 输出格式为FLV
        output_url  # RTMP服务器的URL
    ]
    
    process = subprocess.Popen(command, stdin=subprocess.PIPE)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        annotations = process_frame(frame, int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), yolov8, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles)
        display_and_save_frame(frame, annotations, None)

        # 将处理后的帧写入ffmpeg进程的stdin
        process.stdin.write(frame.tobytes())

    cap.release()
    process.stdin.close()
    process.wait()



def main():
    camera_para = [113.2272883, 21.94803, 100]  # 相机参数 (经度, 纬度, 水平朝向)
    api = ShipServiceAPI()
    ships_data = api.get_nearby_ships("413867644")  # 假设这里返回的ships_data包含mmsi字段

    if not isinstance(ships_data, list):  # 确保API调用成功
        print("API call failed:", ships_data)
        return

    # 将数据转换为DataFrame
    target_points = pd.DataFrame({
        'lon': [ship['longitude'] for ship in ships_data],
        'lat': [ship['latitude'] for ship in ships_data],
        'mmsi': [ship['maritimeMobileServiceIdentity'] for ship in ships_data]
    })
    results = calculate_relative_positions(target_points, camera_para)
    angle_mmsi_mapping = {float(row['angle_with_x_axis']): row['mmsi'] for index, row in results.iterrows()}
    distance_mmsi_mapping = {row['mmsi']: row['distance'] for index, row in results.iterrows()}

    YOLOV8_WEIGHTS = "autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755/onnx/ship_yolov8.onnx"  # 替换为你的模型路径
    DET_THRES = 0.35
    device_no = "hw_mera0813_0"
    url = api.get_camera_video_stream(device_no)

    if not url:
        print("Failed to get video stream URL.")
        return

    cap, yolov8, out = initialize_video_stream(url, YOLOV8_WEIGHTS, DET_THRES, "path_to_output_video.avi")
    if cap is None:
        return

    # 初始化matched_angles
    matched_angles = set()

    stream_video_to_rtmp('rtmp://192.168.1.202:11935/myapp/test', cap, yolov8, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
