# Copyright (c) Facebook, Inc. and its affiliates.
# Copyright (c) Meta Platforms, Inc. All Rights Reserved
# forked & modified by KWTK 202309 for easy use
# using CLIP

import multiprocessing as mp

import numpy as np
from PIL import Image
import os
from typing import Tuple

from detectron2.config import get_cfg

from detectron2.projects.deeplab import add_deeplab_config
from detectron2.data.detection_utils import read_image
from open_vocab_seg import add_ovseg_config
from open_vocab_seg.utils import VisualizationDemo


# ckpt_url = 'https://drive.google.com/uc?id=1cn-ohxgXDrDfkzC1QdO-fi8IjbjXmgKy'
# output = './ovseg_swinbase_vitL14_ft_mpt.pth'
# gdown.download(ckpt_url, output, quiet=False)


__all__ = ['OvSegEasyuse']

def setup_cfg(config_file):
    # load config from file and command-line arguments
    cfg = get_cfg()
    add_deeplab_config(cfg)
    add_ovseg_config(cfg)
    cfg.merge_from_file(config_file)
    cfg.freeze()
    return cfg

class OvSegEasyuse:
    def __init__(self,
                 class_definition: dict,
                 cfg_file: str = './ovseg_swinB_vitL_demo.yaml', 
                 ) -> None:
        assert len(class_definition) < 255, '一次性最多输入254个类别'
        self.class_names, self.class_colors = [], []
        for k, v in class_definition.items():
            self.class_names.append(k.strip())
            assert isinstance(v, list) and len(v) == 3, '颜色必须是长度为3的列表'
            self.class_colors.append(np.array(v))
        mp.set_start_method("spawn", force=True)
        cfg = setup_cfg(cfg_file)
        self.__demo = VisualizationDemo(cfg)


    def inference_and_save(self, 
                           img_path: str, 
                           out_path: str,
                           masked_input_path: str = None) -> np.ndarray:
        vis_image = self.inference(img_path)  # 这将返回一个 VisImage 对象
        self.save_vis_image(vis_image, out_path)  # 调用新的保存方法
        print('finish')

    def save_masked_input(self, 
                          seg: np.ndarray, 
                          img: np.ndarray, 
                          out_path: str) -> None:
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        img = img[:,:,::-1].copy()
        for i, (class_name, class_color) in enumerate(zip(self.class_names, self.class_colors)):
            indices = (seg == i)
            img[indices] = img[indices]*0.5 + class_color*0.5 
        img = Image.fromarray(np.uint8(img)).convert('RGB')
        img.save(out_path)


    # def inference(self, 
    #               img_path: str,
    #               return_img: bool = False) -> np.ndarray or Tuple[np.ndarray, np.ndarray]:
    #     assert os.path.exists(img_path), f"{img_path} 不存在"
    #     img = read_image(img_path, format="BGR")
    #     seg = self.__demo.run_on_image(img, self.class_names)
    #     if return_img:
    #         return seg, img
    #     else:
    #         return seg
        

    def inference(self, 
                img,  # 直接接收图像数据，类型为numpy.ndarray
                return_img: bool = False) -> np.ndarray or Tuple[np.ndarray, np.ndarray]:
        assert img is not None, "图像不能为空"
        seg = self.__demo.run_on_image(img, self.class_names)
        if return_img:
            return seg, img
        else:
            return seg
    
    def save_seg(self, 
                  seg: np.ndarray, 
                  out_path: str) -> None:
        out_img = np.empty((seg.shape[0], seg.shape[1], 3))
        out_img[seg==255] = [0,0,0]
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for i, (class_name, class_color) in enumerate(zip(self.class_names, self.class_colors)):
            out_img[seg == i] = class_color
        out_img = Image.fromarray(np.uint8(out_img)).convert('RGB')
        out_img.save(out_path)

    def save_vis_image(self, vis_image, out_path: str):
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        img = vis_image.get_image()  # 假设 VisImage 有一个 get_image 方法返回图像数据
        img = Image.fromarray(img).convert('RGB')
        img.save(out_path)
