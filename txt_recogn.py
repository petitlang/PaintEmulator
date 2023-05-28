# Add MouZheng's code
import torch
import cv2
import numpy as np
from yolov5.utils.general import non_max_suppression
from yolov5.models.experimental import attempt_load
import tkinter as tk
from PIL import Image, ImageTk
import time

class TextDetector():
    def __init__(self, image):
        self.image = np.array(image)
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        
        # Read the image
        original_frame = self.image
        
        # Create a window named "Settings"
        cv2.namedWindow("Settings", cv2.WINDOW_NORMAL)

        # Create sliders for "conf_thres" and "iou_thres"
        def nothing(x):
            pass

        cv2.createTrackbar("conf_thres", "Settings", 30, 100, nothing)
        cv2.createTrackbar("iou_thres", "Settings", 20, 100, nothing)
        
        while True:
            start_time = time.time()  # Record the start time

            conf_thres = cv2.getTrackbarPos("conf_thres", "Settings") / 100
            iou_thres = cv2.getTrackbarPos("iou_thres", "Settings") / 100

            # Add text to the settings image
            settings_image = np.zeros((300, 512, 3), np.uint8)
            cv2.putText(settings_image, 'Press "q" to close the window', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(settings_image, '"conf_thres" controls the', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(settings_image, 'confidence threshold', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(settings_image, '"iou_thres" controls the IOU', (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(settings_image, 'threshold for non-max suppression', (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Preprocess the frame
            def preprocess_image(image):
                input_size = 640  # yolov5 requires the input image size to be 640
                h, w = image.shape[:2]

                # Convert the image to grayscale if it is not already
                if len(image.shape) > 2:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Apply binary thresholding
                _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
                
                # Reverse black and white areas
                image = cv2.bitwise_not(image)

                aspect_ratio = input_size / max(h, w)  # Calculate scaling ratio
                resized_h, resized_w = int(h * aspect_ratio), int(w * aspect_ratio)  # Resize image
                image = cv2.resize(image, (resized_w, resized_h))

                pad_h = input_size - resized_h  # Pad image
                pad_w = input_size - resized_w
                if pad_h > 0 or pad_w > 0:
                    image = cv2.copyMakeBorder(image, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=0)

                # Convert the processed image to float format and keep the values between 0 and 1.
                image = image.astype(np.float32) / 255.0
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)  # Convert grayscale image to RGB
                image = image.transpose(2, 0, 1)
                image = np.expand_dims(image, axis=0)
                image = torch.from_numpy(image).to(self.device)
                return image

            weights = 'best.pt'
            model = attempt_load(weights)  # Load trained model
            model.to(self.device)
            # Labels
            labels = {
                0: '0',
                1: '1',
                2: '2',
                3: '3',
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: 'A',
                11: 'B',
                12: 'C',
                13: 'D',
                14: 'E',
                15: 'F',
                16: 'G',
                17: 'H',
                18: 'I',
                19: 'J',
                20: 'K',
                21: 'L',
                22: 'M',
                23: 'N',
                24: 'O',
                25: 'P',
                26: 'Q',
                27: 'R',
                28: 'S',
                29: 'T',
                30: 'U',
                31: 'V',
                32: 'W',
                33: 'X',
                34: 'Y',
                35: 'Z',
                36: 'a',
                37: 'b',
                38: 'c',
                39: 'd',
                40: 'e',
                41: 'f',
                42: 'g',
                43: 'h',
                44: 'i',
                45: 'j',
                46: 'k',
                47: 'l',
                48: 'm',
                49: 'n',
                50: 'o',
                51: 'p',
                52: 'q',
                53: 'r',
                54: 's',
                55: 't',
                56: 'u',
                57: 'v',
                58: 'w',
                59: 'x',
                60: 'y',
                61: 'z'
            }
    
            # Create a copy of the original frame
            frame = np.copy(original_frame)

            # Preprocess the frame
            img = preprocess_image(frame)

            ratio = max(frame.shape[0], frame.shape[1]) / 640
                
            # Use yolov5s.pt model for detection
            pred = model(img)[0]

            pred = non_max_suppression(pred, conf_thres=conf_thres, iou_thres=iou_thres, classes=None, agnostic=False, max_det=100)  # Remove overlapping boxes
            
            # show in terminal
            print(pred)
            
            info_text = "No detection"
            # Loop through the detections
            for i, det in enumerate(pred):
                if det is not None and len(det):
                    for x1, y1, x2, y2, conf, cls in reversed(det):
                        x1 = int(x1 * ratio)
                        y1 = int(y1 * ratio)
                        x2 = int(x2 * ratio)
                        y2 = int(y2 * ratio)
                        label = f"{labels[int(cls)]}: {conf:.2f}"
                        # Display label and bounding box coordinates
                        info_text = f"Class: {labels[int(cls)]}, Position: ({x1}, {y1}, {x2}, {y2})"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                        # Check if the text will go out of bounds, and adjust the position if necessary
                        text_width, text_height = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
                        if x1 + text_width > frame.shape[1]:
                            x1 = frame.shape[1] - text_width
                        if y1 - text_height < 0:
                            y1 = text_height + 10

                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            # Display the annotated frame and the processing time in the bottom right corner
            end_time = time.time()  # Record the end time
            time_taken = end_time - start_time
            text_width, text_height = cv2.getTextSize(f"Time taken: {time_taken:.2f} sec", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            cv2.putText(frame, "Time taken: {:.2f} sec".format(time_taken), (frame.shape[1] - text_width - 10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            cv2.imshow("Settings", settings_image)
            
            print(info_text)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
