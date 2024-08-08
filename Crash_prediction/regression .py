import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# 加载数据
data = pd.read_excel('AIS_DEVICE_MESSAGE.xlsx')

# 确保时间戳是 pandas 的 datetime 类型
data['timestamp'] = pd.to_datetime(data['timestamp'])

# 只关注这两艘船的 MMSI
focused_mmsis = [413848169, 413859423]

# 初始化图表
plt.figure(figsize=(10, 6))
collision_points = []

for mmsi in focused_mmsis:
    specific_data = data[data['mmsi'] == mmsi]
    if len(specific_data) < 15:
        continue
    specific_data = specific_data.sort_values(by='timestamp', ascending=True).tail(4)
    specific_data['hours_since_start'] = (specific_data['timestamp'] - data['timestamp'].min()).dt.total_seconds() / 3600
    t = specific_data['hours_since_start'].values.reshape(-1, 1)
    longitude = specific_data['longitude'].values
    latitude = specific_data['latitude'].values
    polynomial_features = PolynomialFeatures(degree=2)
    t_poly = polynomial_features.fit_transform(t)
    model_lon = LinearRegression().fit(t_poly, longitude)
    model_lat = LinearRegression().fit(t_poly, latitude)
    last_time_point = t[-1, 0]  # Use the last time point from real data
    future_time = np.linspace(last_time_point, last_time_point + 15/60, 100)
    future_time_poly = polynomial_features.transform(future_time.reshape(-1, 1))
    predicted_longitude = model_lon.predict(future_time_poly)
    predicted_latitude = model_lat.predict(future_time_poly)
    plt.plot(longitude, latitude, 'o-', label=f'Real Data MMSI {mmsi}')
    plt.plot(predicted_longitude, predicted_latitude, '-', label=f'Predicted Trajectory MMSI {mmsi}')

    # 检测潜在的碰撞
    for other_mmsi in focused_mmsis:
        if other_mmsi != mmsi:
            other_data = data[data['mmsi'] == other_mmsi]
            if len(other_data) < 15:
                continue
            other_data = other_data.sort_values(by='timestamp', ascending=True).tail(4)
            other_data['hours_since_start'] = (other_data['timestamp'] - data['timestamp'].min()).dt.total_seconds() / 3600
            other_t = other_data['hours_since_start'].values.reshape(-1, 1)
            other_longitude = other_data['longitude'].values
            other_latitude = other_data['latitude'].values
            other_t_poly = polynomial_features.fit_transform(other_t)
            other_model_lon = LinearRegression().fit(other_t_poly, other_longitude)
            other_model_lat = LinearRegression().fit(other_t_poly, other_latitude)
            other_future_time_poly = polynomial_features.transform(future_time.reshape(-1, 1))
            other_predicted_longitude = other_model_lon.predict(other_future_time_poly)
            other_predicted_latitude = other_model_lat.predict(other_future_time_poly)
            for i in range(100):
                dist = geodesic((predicted_latitude[i], predicted_longitude[i]), (other_predicted_latitude[i], other_predicted_longitude[i])).meters
                if dist < 10:
                    collision_points.append((predicted_longitude[i], predicted_latitude[i]))
                    plt.plot(predicted_longitude[i], predicted_latitude[i], 'rx', markersize=10, label='Collision Point' if i == 0 else "")

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Trajectory Analysis with Potential Collision Detection')
plt.legend()
plt.grid(True)
plt.show()
