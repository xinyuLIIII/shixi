import requests

class ShipServiceAPI:
    def __init__(self, base_url, auth_code):
        self.base_url = base_url
        self.headers = {"Authorization": auth_code}

    def get_nearby_ships(self, mmsi):
        """获取附近的船舶"""
        url = f"{self.base_url}/ais/ships-nearby?mmsi={mmsi}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                return data['ships']
            else:
                return "Error: API returned an error."
        else:
            return "Error: Failed to fetch data."

    def get_ship_cameras(self, ship_name):
        """获取船舶摄像头列表"""
        url = f"{self.base_url}/ship-video/cameras?shipName={ship_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                return data['cameras']
            else:
                return "Error: API returned an error."
        else:
            return "Error: Failed to fetch data."

    def get_camera_video_stream(self, device_no):
        """获取摄像头的实时视频流"""
        url = f"{self.base_url}/ship-video/video-url?deviceNo={device_no}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                return data['video']
            else:
                return "Error: API returned an error."
        else:
            return "Error: Failed to fetch data."

# 使用示例
base_url = ""  # 替换服务地址
auth_code = ""  # 替换授权码

api = ShipServiceAPI(base_url, auth_code)
mmsi = ""  # 替换为具体的MMSI码
ship_name = ""  # 替换为具体的船名
device_no = ""  # 替换为具体的设备编号

print(api.get_nearby_ships(mmsi))
print(api.get_ship_cameras(ship_name))
print(api.get_camera_video_stream(device_no))
