import pandas as pd

# 读取数据，处理连续逗号表示的空字段
data = pd.read_csv('Crash_prediction\AIS_DEVICE_MESSAGE.csv', sep=',', skipinitialspace=True, keep_default_na=True)

# 查看数据的前几行和列信息以确认数据正确加载
print(data.head())
print(data.info())

# 过滤出特定 mmsi 的数据
specific_mmsi = 413867644
filtered_data = data[data['mmsi'] == specific_mmsi]

# 检查过滤后的数据
if filtered_data.empty:
    print("没有找到指定MMSI的数据。请检查MMSI号是否正确。")
else:
    print("过滤后的数据:")
    print(filtered_data.head())
