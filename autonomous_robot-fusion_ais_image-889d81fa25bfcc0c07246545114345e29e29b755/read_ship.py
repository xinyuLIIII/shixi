import json
import time

def read_and_process_data(filename, interval=5):
    """逐段读取文件数据，并在每次读取前清空之前的数据，每段之后暂停一定时间"""
    with open(filename, 'r') as file:
        current_block = []  # 用于存储当前读取的数据块

        for line in file:
            stripped_line = line.strip()
            if stripped_line == '---':
                if current_block:
                    process_data_block(current_block)  # 处理当前数据块
                    current_block = []  # 清空数据块以用于下一个
                    time.sleep(interval)  # 每个数据块处理后暂停
            else:
                current_block.append(stripped_line)  # 继续添加数据到当前块

        # 处理最后一个数据块（如果存在）
        if current_block:
            process_data_block(current_block)

def process_data_block(block):
    """处理每个独立的数据块，并将其转换为字典"""
    json_data = []  # 初始化空列表以存储JSON解析结果
    for line in block:
        try:
            if line.startswith('[') and line.endswith(']'):
                json_data = json.loads(line)  # 解析JSON数据
                print(json_data)  # 打印转换后的字典
        except json.JSONDecodeError as e:
            print("JSON解析错误：", e)
            print("导致错误的数据：", line)

    # 这里可以添加任何你想对json_data进行的操作
    # 如分析数据，保存到数据库等

# 使用示例
if __name__ == '__main__':
    read_and_process_data('ships_data.txt', interval=5)
