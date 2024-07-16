import pandas as pd
from API import ShipServiceAPI
from math import radians, degrees, atan2, sin, cos
from geopy.distance import geodesic

def count_distance(point1: tuple, point2: tuple, unit: str = 'm') -> float:
    distance = geodesic(point1, point2).meters
    if unit == 'nm':
        distance *= 0.00054
    return distance

def get_degree(latA: float, lonA: float, latB: float, lonB: float) -> float:
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    return (brng + 360) % 360

def calculate_relative_positions(target_points: pd.DataFrame, camera_para: list) -> pd.DataFrame:
    lon_cam, lat_cam, shoot_hdir = camera_para
    results = []
    for index, row in target_points.iterrows():
        lon_v, lat_v, mmsi_v = row['lon'], row['lat'], row['mmsi']
        D_abs = count_distance((lat_cam, lon_cam), (lat_v, lon_v))
        if D_abs <= 1000:  # 过滤大于500米的目标点
            relative_angle = get_degree(lat_cam, lon_cam, lat_v, lon_v)
            Angle_hor = relative_angle - shoot_hdir
            if Angle_hor < -180:
                Angle_hor += 360
            elif Angle_hor > 180:
                Angle_hor -= 360

            # 过滤绝对角度大于90或小于-90的目标点
            if -90 <= Angle_hor <= 90:
                hor_rad = radians(Angle_hor)
                X_w = D_abs * sin(hor_rad)
                Y_w = D_abs * cos(hor_rad)
                angle_with_x_axis = float(degrees(atan2(X_w, Y_w)))  # 确保角度是浮点数
                results.append((lon_v, lat_v, mmsi_v, D_abs, angle_with_x_axis))
    return pd.DataFrame(results, columns=['lon', 'lat', 'mmsi', 'distance', 'angle_with_x_axis'])



