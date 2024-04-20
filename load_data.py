import os
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image
from sklearn.model_selection import train_test_split

def train (images_dir,masks_dir):
    
    all_image_file_names = sorted(os.listdir(images_dir))
    target_size = (128, 128)
    images = [np.array(Image.open(os.path.join(images_dir, fname)).resize(target_size)) for fname in all_image_file_names]
    mask_file_names = [fname.replace('.jpg', '_mask.png') for fname in all_image_file_names]
    masks = [np.array(Image.open(os.path.join(masks_dir, fname)).resize(target_size)) for fname in mask_file_names]
    images = np.array(images)
    masks = np.array(masks)
    images = images / 255.0
    if masks.shape[-1] == 3:
        masks = np.mean(masks, axis=-1, keepdims=True)
    masks = masks.reshape((masks.shape[0], masks.shape[1], masks.shape[2], 1))
    x_train, x_temp, y_train, y_temp = train_test_split(images, masks, test_size=0.3, random_state=42)
    x_valid, x_test, y_valid, y_test = train_test_split(x_temp, y_temp, test_size=1/3, random_state=42)
    return x_test,y_test
