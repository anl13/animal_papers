import cv2 
import numpy as np 
import os 
from tqdm import tqdm 

def compress():
    source_dir = "teasers"
    target_dir = "teasers_small"
    data = os.listdir(source_dir)
    for d in tqdm(data): 
        src_filename = os.path.join(source_dir, d) 
        tgt_filename = os.path.join(target_dir, d) 
        img = cv2.imread(src_filename) 
        H = img.shape[0] 
        W = img.shape[1] 
        W_small = 300
        ratio = W_small / W 
        H_small = int(H * ratio)
        H_small = H_small // 2 * 2 
        img_small = cv2.resize(img, (W_small, H_small))
        cv2.imwrite(tgt_filename, img_small)


if __name__ == "__main__": 
    compress() 