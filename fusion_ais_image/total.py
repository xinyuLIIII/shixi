import subprocess
import cv2
import pandas as pd
from ship_utils import calculate_relative_positions
from API import ShipServiceAPI
from yolo_utils import initialize_video_stream, process_frame, display_and_save_frame
from collections import defaultdict
import numpy as np
from scipy.interpolate import interp1d
import app

accumulated_distances = defaultdict(list)
last_recorded_distances = {}
interpolated_distances = defaultdict(list)
final_distances = {}

def ais_data_con(api, camera_para, mmsi):
    ships_data = api.get_nearby_ships(mmsi)

    if not isinstance(ships_data, list):
        print("API call failed:", ships_data)
        return None

    target_points = pd.DataFrame({
        'lon': [ship['longitude'] for ship in ships_data],
        'lat': [ship['latitude'] for ship in ships_data],
        'mmsi': [ship['maritimeMobileServiceIdentity'] for ship in ships_data]
    })

    results = calculate_relative_positions(target_points, camera_para)
    angle_mmsi_mapping = {float(row['angle_with_x_axis']): row['mmsi'] for index, row in results.iterrows()}

    for index, row in results.iterrows():
        accumulated_distances[row['mmsi']].append(row['distance'])

    # Update and interpolate distances
    for mmsi, distances in accumulated_distances.items():
        if len(distances) >= 4:
            x = np.arange(len(distances))
            f = interp1d(x, distances, kind='cubic', fill_value="extrapolate")
            fine_x = np.linspace(0, len(distances) - 1, num=len(distances) * 10)
            interpolated_result = f(fine_x)
            interpolated_distances[mmsi] = interpolated_result
            final_distances[mmsi] = interpolated_result[-1]
        elif len(distances) > 1:
            x = np.arange(len(distances))
            f = interp1d(x, distances, kind='linear')
            fine_x = np.linspace(0, len(distances) - 1, num=len(distances) * 10)
            interpolated_result = f(fine_x)
            interpolated_distances[mmsi] = interpolated_result
            final_distances[mmsi] = interpolated_result[-1]
        elif distances:
            final_distances[mmsi] = distances[0]

    return angle_mmsi_mapping

def ffmpeg_init(output_url, cap):
    command = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', '{}x{}'.format(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),
        '-r', '1',
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-f', 'flv',
        output_url
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    return process

def process_data(output_url, out,cap, yolov8, matched_angles, api, camera_para, mmsi):
    #process = ffmpeg_init(output_url, cap)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            angle_mmsi_mapping = ais_data_con(api, camera_para, mmsi)
            if angle_mmsi_mapping is None:
                print("Failed to get ship data.")
                continue
            #print(interpolated_distances)
            annotations = process_frame(frame, int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), yolov8, angle_mmsi_mapping, final_distances,interpolated_distances,matched_angles)
            display_and_save_frame(frame, annotations, out)
            # process.stdin.write(frame.tobytes())
    finally:
        cap.release()
        # process.stdin.close()
        # process.wait()
        print("Cleanup complete.")

def main():
    camera_para = [111.1406267,23.43458,327]
    api = ShipServiceAPI()
    mmsi = "413848169"
    yolov8_weights = "fusion_ais_image/onnx/best.onnx"
    det_thres = 0.35
    device_no = "hw_mera0821_1"
    url = api.get_camera_video_stream(device_no)

    if not url:
        print("Failed to get video stream URL.")
        return

    cap, yolov8, out = initialize_video_stream(url, yolov8_weights, det_thres, "fusion_ais_image/video/output_video_6.avi")
    if cap is None:
        return

    matched_angles = set()

    process_data('rtmp://192.168.1.202:11935/myapp/test', out,cap, yolov8, matched_angles, api, camera_para, mmsi)

    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    app.run(debug=True)
    main()
