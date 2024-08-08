import requests

class ShipServiceAPI:
    def __init__(self):
        self.base_url = "https://wxapptest.kinthtech.com.cn/apserver"
        self.headers = {"Authorization": "cb04b04bdd6544f9b93b2e32bab543e7"}

    def get_nearby_ships(self, mmsi):
        """获取附近的船舶"""
        url = f"{self.base_url}/ais/ships-nearby?mmsi={mmsi}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Response Code: {data['code']}")  # 打印code值
            if data['code'] == 0:
                ships = data['ships']
                return ships
            else:
                return f"Error: API returned an error. Code: {data['code']}"
        else:
            return f"Error: Failed to fetch data. HTTP Status: {response.status_code}"
        
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
                video_info = data['video']
                #return data['video']
                if 'url' in video_info:
                    return video_info['url']  # 返回视频流的URL
                else:
                    return "Error: URL not found in the response."
            else:
                return "Error: API returned an error. Code: " + str(data['code'])
        else:
            return "Error: Failed to fetch data. HTTP Status: " + str(response.status_code)


if __name__ == '__main__':
    api = ShipServiceAPI()
    mmsi = "413873583"  # 替换为具体的MMSI码
    ship_name = "粤海10"  # 替换为具体的船名
    device_no = "hw_mera0862_0"  # 替换为具体的设备编号
    print(api.get_nearby_ships(mmsi))
    #print(api.get_ship_cameras(ship_name))
    #print(api.get_camera_video_stream(device_no))


