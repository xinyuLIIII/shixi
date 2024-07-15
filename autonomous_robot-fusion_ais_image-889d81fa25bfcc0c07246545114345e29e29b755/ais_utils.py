from math import radians, degrees, atan2, sin, cos
from geopy.distance import geodesic
import pandas as pd

def count_distance(point1: tuple, point2: tuple, unit: str = 'm') -> float:
    """
    功能: 使用经纬度计算两点间的距离
    参数:
        point1: 点1的经纬度（经度，纬度）
        point2: 点2的经纬度（经度，纬度）
        unit: 距离单位，'nm' 表示海里, 'm' 表示米
    返回值: 二者之间的距离，单位为指定的单位
    """
    distance = geodesic(point1, point2).meters  # 计算两点间的距离，单位为米
    if unit == 'nm':
        distance *= 0.00054  # 将距离转换为海里
    return distance

def get_degree(latA: float, lonA: float, latB: float, lonB: float) -> float:
    """
    功能: 计算两点间方位角
    参数:
        latA: 点A的纬度
        lonA: 点A的经度
        latB: 点B的纬度
        lonB: 点B的经度
    返回值: 方位角，单位为度
    """
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
    """
    功能: 计算多个目标点相对于相机的距离和与x轴的夹角
    参数:
        target_points: 多个目标点的经纬度 (DataFrame)
        camera_para: 相机参数列表 [lon_cam, lat_cam, shoot_hdir]
    返回值: 包含每个目标点相对于相机的距离和与x轴夹角的DataFrame
    """
    lon_cam, lat_cam, shoot_hdir = camera_para
    results = []

    for index, row in target_points.iterrows():
        lon_v, lat_v = row['lon'], row['lat']
        D_abs = count_distance((lat_cam, lon_cam), (lat_v, lon_v))
        relative_angle = get_degree(lat_cam, lon_cam, lat_v, lon_v)
        Angle_hor = relative_angle - shoot_hdir
        if Angle_hor < -180:
            Angle_hor += 360
        elif Angle_hor > 180:
            Angle_hor -= 360
        hor_rad = radians(Angle_hor)
        X_w = D_abs * sin(hor_rad)
        Y_w = D_abs * cos(hor_rad)
        angle_with_x_axis = degrees(atan2(X_w, Y_w))
        results.append((lon_v, lat_v, D_abs, angle_with_x_axis))

    return pd.DataFrame(results, columns=['lon', 'lat', 'distance', 'angle_with_x_axis'])

# 示例使用
camera_para = [114.32583, 30.60139, 353]  # 相机参数 (经度, 纬度, 水平朝向)
target_points = pd.DataFrame({
    'lon': [114.326283,114.322247,114.33309,114.32533],
    'lat': [30.611185,30.609772,30.617163,30.601673
]
})

results = calculate_relative_positions(target_points, camera_para)
print(results)
