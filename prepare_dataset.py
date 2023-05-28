import numpy as np
import os
import cv2
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from torchvision.datasets import EMNIST
from torchvision import transforms
import torch
import matplotlib.pyplot as plt
from PIL import Image

def create_blank(width, height, color=0):
    image = np.full((height, width), color, dtype=np.uint8)
    return image

def place_images(blank_img, emnist_data, max_images=10, max_attempts=100):
    labels = []
    # Create an empty mask to keep track of occupied spaces
    used_mask = np.zeros(blank_img.shape, dtype=bool)
    for _ in range(np.random.randint(1, max_images)):
        # Get random image from EMNIST
        index = np.random.randint(0, len(emnist_data))
        img, label = emnist_data[index]

        # Convert to numpy array, ensure it's grayscale (single channel), scale values to 0-255, and convert to uint8
        img = (np.array(img)[0] * 255).astype(np.uint8)

        # Rotate and flip the image
        img = np.rot90(img)
        img = np.flipud(img)

        # Resize randomly
        scale_x = np.random.uniform(6, 12)
        scale_y = np.random.uniform(6, 12)
        img = cv2.resize(img, None, fx=scale_x, fy=scale_y)

        # Try to get random coordinates to place image on blank
        attempt = 0
        while attempt < max_attempts:
            x, y = np.random.randint(0, blank_img.shape[1] - img.shape[1] + 1), np.random.randint(0, blank_img.shape[0] - img.shape[0] + 1)
            # Check if image overlaps with any previous images
            if not np.any(used_mask[y:y+img.shape[0], x:x+img.shape[1]]):
                break
            attempt += 1
        else:
            # Skip this image if we can't find a place for it after max_attempts
            continue

        # Add image coordinates to used_coords
        used_mask[y:y+img.shape[0], x:x+img.shape[1]] = True

        # Place image on blank
        blank_img[y:y+img.shape[0], x:x+img.shape[1]] = img

        # Save label in yolov5 format (class, center_x, center_y, width, height)
        labels.append([label, (x+img.shape[1]/2)/640, (y+img.shape[0]/2)/640, img.shape[1]/640, img.shape[0]/640])

    return blank_img, labels

def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def create_datasets(num_data):
    ensure_dir('NewDataset')
    dirs = ['train', 'valid', 'test']
    for dir_name in dirs:
        ensure_dir(os.path.join('NewDataset', dir_name))
        ensure_dir(os.path.join('NewDataset', dir_name, 'labels'))
        ensure_dir(os.path.join('NewDataset', dir_name, 'images'))

    emnist_data = EMNIST(root='.', split='byclass', download=True, transform=transforms.ToTensor())

    for i in tqdm(range(num_data)):
        blank_img = create_blank(640, 640)
        img, labels = place_images(blank_img, emnist_data)

        if i < num_data*0.8:
            dir_name = 'train'
        elif i < num_data*0.9:
            dir_name = 'valid'
        else:
            dir_name = 'test'

        img = Image.fromarray(img)
        img.save(f'NewDataset/{dir_name}/images/{i}.png')

        with open(f'NewDataset/{dir_name}/labels/{i}.txt', 'w') as f:
            for label in labels:
                f.write(' '.join([str(l) for l in label]) + '\n')


create_datasets(num_data=20000)
