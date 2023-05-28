# Text Recognition Script - README

This script, named "txt_recogn.py," is part of a project that enables text detection and recognition in an image. When the project activates this functionality, an image is passed to this script for processing. And we add a timer to show the token time.

This project includes a script named `txt_recogn.py`, which uses a weights file called `best.pt`. This weights file is trained on a dataset created by the script `prepare_dataset.py`.

## Prerequisites

Before running this script, ensure that you have the following dependencies installed:

- Python (3.x)
- OpenCV (`cv2`)
- NumPy
- PyTorch
- tkinter
- Pillow (`PIL`)
- YOLOv5
- time

You can install the required Python libraries using pip:

```
pip install opencv-python numpy torch pillow yolov5
```

Make sure you have the YOLOv5 model weights (`best.pt`) in the same directory as the script.

## Usage

To use this script, follow these steps:

The script can be used on its own or, if used alone, it requires (skip to step 4 if you use with our project):

1. Import the necessary libraries:

```python
import torch
import cv2
import numpy as np
from yolov5.utils.general import non_max_suppression
from yolov5.models.experimental import attempt_load
import tkinter as tk
from PIL import Image, ImageTk
import time
```

2. Instantiate the `TextDetector` class and provide it with the image to process:

```python
image = Image.open('path/to/image.jpg')
text_detector = TextDetector(image)
```

3. Run the script:

```python
text_detector.run()
```

If you use with our project, when you finish your paint, chose select to chose a zone you want to do recognition, and click "Start Analysing", then: 

4. A window will open displaying the original image with bounding boxes and labels around detected text regions. Additionally, a settings window will appear, allowing you to adjust the confidence threshold (`conf_thres`) and IOU threshold (`iou_thres`) using trackbars. Use these trackbars to fine-tune the text detection parameters.

5. Press 'q' to close the windows and exit the script.

Note: The script assumes that the YOLOv5 model weights (`best.pt`) are present in the current directory. Make sure to download the weights or provide the correct path if they are stored elsewhere.

## Additional Information

- The script utilizes YOLOv5 for text detection. It loads the model weights and performs non-maximum suppression on the predicted bounding boxes to remove overlapping boxes.
- Detected text regions are labeled with their corresponding class and confidence score.
- The script supports both CPU and GPU acceleration. It automatically selects the available device (CUDA GPU if available, otherwise CPU).
- The detected text regions and their corresponding information are printed in the terminal.
- The script uses the tkinter library to create the user interface and display the image windows.

Feel free to modify and integrate this script into your project to enable text detection and recognition functionality.

For more information on YOLOv5 and its usage, refer to the official YOLOv5 repository: https://github.com/ultralytics/yolov5



## Prepare Dataset Script

The `prepare_dataset.py` script is designed to generate a synthetic dataset suitable for training a text recognition model. Here's a brief overview of what it does:

1. It creates a blank image of a specified size.
2. It randomly selects images from the EMNIST dataset, which is a large set of handwritten characters and digits.
3. Each selected image is manipulated in various ways (rotated, flipped, resized) and then randomly placed on the blank image.
4. It creates a label for each placed image in the YOLOv5 format, which includes the class and the position and size of the bounding box.
5. It saves the final image and the associated labels to the appropriate directories for training, validation, and testing.

The script is run with the command `create_datasets(num_data=20000)`, which creates a total of 20,000 images for the dataset.

## Best.pt Weights File

The `best.pt` weights file used by `txt_recogn.py` is obtained by training a YOLOv5 model on the dataset created by `prepare_dataset.py`. 

This model is trained with `yolov5.pt` as a pre-trained weights file. The `yolov5.pt` file contains weights trained on a large and diverse dataset, which provides a good starting point for the training process. Using this pre-trained model speeds up training and often leads to better performance.

Please note that the `best.pt` weights file is specifically tuned to the dataset created by `prepare_dataset.py`, and may not work as well with different datasets or tasks.
