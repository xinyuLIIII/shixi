import cv2
import pandas as pd
from ship_utils import calculate_relative_positions
from API import ShipServiceAPI
from yolo_utils import initialize_video_stream, process_frame, display_and_save_frame
import asyncio
from aiohttp import web
from queue import Queue
import threading

# 创建全局FIFO队列
fifo_queue = Queue()

async def mjpeg_handler(request):
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame'
    })
    await response.prepare(request)
    try:
        while True:
            if not fifo_queue.empty():
                frame = fifo_queue.get()
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                data = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n'
                await response.write(data)
                await asyncio.sleep(0.05)  # 控制帧率
    except Exception as e:
        print('Stream closed:', e)
    finally:
        await response.write_eof()

async def start_app():
    app = web.Application()
    app.router.add_get('/video', mjpeg_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

def video_processing(cap, yolov8, out, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        annotations = process_frame(frame, cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT), yolov8, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles)
        display_and_save_frame(frame, annotations, out)
        fifo_queue.put(frame)  # 将处理后的帧放入队列

def main():
    camera_para = [112.5105567, 23.0522717, 55]  # 相机参数
    api = ShipServiceAPI()
    ships_data = api.get_nearby_ships("413860512")

    if not isinstance(ships_data, list):
        print("API call failed:", ships_data)
        return

    target_points = pd.DataFrame({
        'lon': [ship['longitude'] for ship in ships_data],
        'lat': [ship['latitude'] for ship in ships_data],
        'mmsi': [ship['maritimeMobileServiceIdentity'] for ship in ships_data]
    })
    results = calculate_relative_positions(target_points, camera_para)
    angle_mmsi_mapping = {float(row['angle_with_x_axis']): row['mmsi'] for index, row in results.iterrows()}
    distance_mmsi_mapping = {row['mmsi']: row['distance'] for index, row in results.iterrows()}

    url = api.get_camera_video_stream("hw_mera0833_1")
    if not url:
        print("Failed to get video stream URL.")
        return

    cap, yolov8, out = initialize_video_stream(url, "autonomous_robot-fusion_ais_image-889d81fa25bfcc0c07246545114345e29e29b755/onnx/ship_yolov8.onnx", 0.35, "output_video.avi")
    if cap is None:
        return

    matched_angles = set()  # Set to keep track of matched angles

    # Start the video processing in a separate thread
    threading.Thread(target=video_processing, args=(cap, yolov8, out, angle_mmsi_mapping, distance_mmsi_mapping, matched_angles)).start()

    # Start the web server
    asyncio.run(start_app())

if __name__ == "__main__":
    main()
