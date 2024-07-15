from __future__ import absolute_import, division, print_function

import os
import numpy as np
import PIL.Image as pil
from PIL import ImageEnhance, ImageOps, ImageFilter
import matplotlib.pyplot as plt

import torch
from torchvision import transforms

import networks

def enhance_image(image):
    # 增加对比度
    enhancer = ImageEnhance.Contrast(image)
    image_enhanced = enhancer.enhance(3.0)  # 对比度系数，可以调整

    # 应用直方图均衡化
    image_eq = ImageOps.equalize(image_enhanced)

    # 应用锐化滤波器
    image_sharpened = image_eq.filter(ImageFilter.SHARPEN)

    return image_sharpened

model_name = "mono+stereo_640x192"

encoder_path = os.path.join("models", model_name, "encoder.pth")
depth_decoder_path = os.path.join("models", model_name, "depth.pth")

# LOADING PRETRAINED MODEL
encoder = networks.ResnetEncoder(18, False)
depth_decoder = networks.DepthDecoder(num_ch_enc=encoder.num_ch_enc, scales=range(4))

loaded_dict_enc = torch.load(encoder_path, map_location='cpu')
filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
encoder.load_state_dict(filtered_dict_enc)

loaded_dict = torch.load(depth_decoder_path, map_location='cpu')
depth_decoder.load_state_dict(loaded_dict)

encoder.eval()
depth_decoder.eval()

image_path = "1720075598013.png"

input_image = pil.open(image_path).convert('RGB')
original_width, original_height = input_image.size

# 图像增强
input_image_enhanced = enhance_image(input_image)

feed_height = loaded_dict_enc['height']
feed_width = loaded_dict_enc['width']
input_image_resized = input_image_enhanced.resize((feed_width, feed_height), pil.LANCZOS)

input_image_pytorch = transforms.ToTensor()(input_image_resized).unsqueeze(0)

with torch.no_grad():
    features = encoder(input_image_pytorch)
    outputs = depth_decoder(features)

disp = outputs[("disp", 0)]
disp_resized = torch.nn.functional.interpolate(disp,
    (original_height, original_width), mode="bilinear", align_corners=False)

# Saving colormapped depth image
disp_resized_np = disp_resized.squeeze().cpu().numpy()
vmax = np.percentile(disp_resized_np, 95)

plt.figure(figsize=(10, 10))
plt.subplot(211)
plt.imshow(input_image_enhanced)
plt.title("Enhanced Input", fontsize=22)
plt.axis('off')

plt.subplot(212)
plt.imshow(disp_resized_np, cmap='magma', vmax=vmax)
plt.title("Disparity prediction", fontsize=22)
plt.savefig('disparity_prediction.png', bbox_inches='tight', pad_inches=0)
plt.close()