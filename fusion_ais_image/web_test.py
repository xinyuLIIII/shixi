import subprocess

def stream_from_camera(rtmp_url):
    # 定义ffmpeg命令，用于捕捉摄像头视频流并推送到RTMP服务器
    command = [
        'ffmpeg',
        '-f', 'v4l2',  # 摄像头捕捉命令，适用于Linux
        '-i', '/dev/video0',  # 摄像头设备文件
        '-c:v', 'libx264',  # 使用x264编码视频流
        '-b:v', '1000k',  # 视频比特率
        '-c:a', 'aac',  # 使用AAC编码音频流
        '-strict', 'experimental',  # 启用实验特性
        '-f', 'flv',  # FLV格式
        rtmp_url  # RTMP服务器的URL
    ]

    # 执行命令
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if output:
        print("STDOUT:", output.decode())
    if error:
        print("STDERR:", error.decode())

if __name__ == "__main__":
    # RTMP服务器的URL
    rtmp_server_url = 'rtmp://localhost/live/stream'
    stream_from_camera(rtmp_server_url)
