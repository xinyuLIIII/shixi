from collections import defaultdict
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import time
from ship_utils import calculate_relative_positions
from API import ShipServiceAPI

# 初始化字典存储每个 mmsi 的累计距离、插值结果和最后记录的距离
accumulated_distances = defaultdict(list)
last_recorded_distances = {}
interpolated_distances = defaultdict(list)
final_distances = {}

def main():
    camera_para = [111.1416933, 23.4367217, 360]
    api = ShipServiceAPI()
    ships_data = api.get_nearby_ships("413848169")

    if not isinstance(ships_data, list):
        print("API call failed:", ships_data)
        return

    target_points = pd.DataFrame({
        'lon': [ship['longitude'] for ship in ships_data],
        'lat': [ship['latitude'] for ship in ships_data],
        'mmsi': [ship['maritimeMobileServiceIdentity'] for ship in ships_data]
    })

    results = calculate_relative_positions(target_points, camera_para)
    new_distances = defaultdict(list)
    for index, row in results.iterrows():
        new_distances[row['mmsi']].append(row['distance'])

    for mmsi, distances in new_distances.items():
        if mmsi not in last_recorded_distances or last_recorded_distances[mmsi] != distances[-1]:
            accumulated_distances[mmsi].extend(distances)
            last_recorded_distances[mmsi] = distances[-1]  # 更新最后记录的距离

    for mmsi, distances in accumulated_distances.items():
        if len(distances) >= 4:
            # 足够的点进行三次样条插值
            x = np.arange(len(distances))
            f = interp1d(x, distances, kind='cubic', fill_value="extrapolate")
            fine_x = np.linspace(0, len(distances) - 1, num=len(distances) * 10)
            interpolated_result = f(fine_x)
            interpolated_distances[mmsi] = interpolated_result
            final_distances[mmsi] = interpolated_result[-1]
        elif len(distances) > 1:
            # 点不足但超过一个，进行线性插值
            x = np.arange(len(distances))
            f = interp1d(x, distances, kind='linear')
            fine_x = np.linspace(0, len(distances) - 1, num=len(distances) * 10)
            interpolated_result = f(fine_x)
            interpolated_distances[mmsi] = interpolated_result
            final_distances[mmsi] = interpolated_result[-1]
        elif distances:
            final_distances[mmsi] = distances[0]  # 只有一个数据点时直接使用它

    print(interpolated_distances)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)  # 循环间隔时间
