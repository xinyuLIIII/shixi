import zipfile
import os
import shutil
from ov_seg_easyuse import OvSegEasyuse

def extract_zip(zip_path, extract_to):
    """解压 ZIP 文件到指定目录"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main(zip_path, output_seg_dir, output_masked_dir, class_definition):
    """处理 ZIP 压缩包中的图片"""
    # 解压 zip 文件
    temp_dir = 'temp_images'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    extract_zip(zip_path, temp_dir)

    # 初始化 OvSegEasyuse 类
    segmenter = OvSegEasyuse(class_definition)

    # 确保输出目录存在
    os.makedirs(output_seg_dir, exist_ok=True)
    os.makedirs(output_masked_dir, exist_ok=True)

    # 遍历解压后的所有图片进行推理
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                out_seg_path = os.path.join(output_seg_dir, file)
                out_masked_path = os.path.join(output_masked_dir, file)
                # 推理并保存结果
                segmenter.inference_and_save(img_path, out_seg_path, out_masked_path)

    # 删除临时目录
    shutil.rmtree(temp_dir)
    print('All images processed and outputs are saved.')

if __name__ == "__main__":
    zip_path = './images.zip'  # 输入的 zip 文件路径
    output_seg_dir = './demo_images_seg'  # 输出分割结果的目录路径
    output_masked_dir = './demo_images_masked'  # 输出掩膜图的目录路径
    class_definition = {
        'shipping': [255, 0, 0],
        'ship':[255, 0, 0]
    }


    main(zip_path, output_seg_dir, output_masked_dir, class_definition)
