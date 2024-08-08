import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# 加载数据
data = pd.read_excel('Crash_prediction/AIS_DEVICE_MESSAGE.xlsx')

# 确保时间戳是 pandas 的 datetime 类型
data['timestamp'] = pd.to_datetime(data['timestamp'])

# 获取所有唯一的 MMSI
unique_mmsis = data['mmsi'].unique()

# 初始化图表
plt.figure(figsize=(15, 10))
collision_points = []

for mmsi in unique_mmsis:
    specific_data = data[data['mmsi'] == mmsi]

    specific_data = specific_data.sort_values(by='timestamp', ascending=True).tail(15)
    specific_data['hours_since_start'] = (specific_data['timestamp'] - specific_data['timestamp'].min()).dt.total_seconds() / 3600
    t = specific_data['hours_since_start'].values.reshape(-1, 1)
    longitude = specific_data['longitude'].values
    latitude = specific_data['latitude'].values
    polynomial_features = PolynomialFeatures(degree=2)
    t_poly = polynomial_features.fit_transform(t)
    model_lon = LinearRegression().fit(t_poly, longitude)
    model_lat = LinearRegression().fit(t_poly, latitude)
    last_time_point = t.max()
    future_time = np.linspace(last_time_point, last_time_point + 15/60, 100)  # 修改为30分钟后
    future_time_poly = polynomial_features.transform(future_time.reshape(-1, 1))
    predicted_longitude = model_lon.predict(future_time_poly)
    predicted_latitude = model_lat.predict(future_time_poly)
    plt.plot(longitude, latitude, 'o-', label=f'Real Data MMSI {mmsi}')
    plt.plot(predicted_longitude, predicted_latitude, '-', label=f'Predicted Trajectory MMSI {mmsi}')
    for other_mmsi in unique_mmsis:
        if other_mmsi != mmsi:
            other_data = data[data['mmsi'] == other_mmsi]
            if len(other_data) < 15:
                continue
            other_data = other_data.sort_values(by='timestamp', ascending=True).tail(15)
            other_data['hours_since_start'] = (other_data['timestamp'] - other_data['timestamp'].min()).dt.total_seconds() / 3600
            other_t = other_data['hours_since_start'].values.reshape(-1, 1)
            other_longitude = other_data['longitude'].values
            other_latitude = other_data['latitude'].values
            other_t_poly = polynomial_features.fit_transform(other_t)
            other_model_lon = LinearRegression().fit(other_t_poly, other_longitude)
            other_model_lat = LinearRegression().fit(other_t_poly, other_latitude)
            other_last_time_point = other_t.max()
            other_future_time = np.linspace(other_last_time_point, other_last_time_point + 15/60, 100)  # 也修改为30分钟后
            other_future_time_poly = polynomial_features.transform(other_future_time.reshape(-1, 1))
            other_predicted_longitude = other_model_lon.predict(other_future_time_poly)
            other_predicted_latitude = other_model_lat.predict(other_future_time_poly)
            for i in range(100):
                if geodesic((predicted_latitude[i], predicted_longitude[i]), (other_predicted_latitude[i], other_predicted_longitude[i])).meters < 10:
                    collision_points.append((predicted_longitude[i], predicted_latitude[i]))
                    print(f"Collision warning between MMSI {mmsi} and {other_mmsi} at ({predicted_longitude[i]}, {predicted_latitude[i]})")
                    plt.plot(predicted_longitude[i], predicted_latitude[i], 'rx', markersize=12)  # Mark collision points

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Predicted Trajectory Maps for Multiple Ships with Collision Warnings')
plt.legend()
plt.grid(True)
plt.show()
