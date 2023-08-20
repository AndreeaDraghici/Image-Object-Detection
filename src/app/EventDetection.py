import logging

import cv2
import numpy as np

from src.LoadLoggingConfig import load_logging_config


class EventDetection :

    def __init__(self) :
        # Load the logging configuration
        load_logging_config()
        # Get the logger for the 'development' logger
        self.logger = logging.getLogger('development')

        try :
            # Initialize the YOLO detector
            self.net = cv2.dnn.readNet('../model/yolov3.cfg', '../model/yolov3.weights')

        except cv2.error as e :
            # Log an error if YOLO initialization fails
            self.logger.error("Failed to initialize YOLO detector: %s", str(e))

        # Initialize an empty list to store class names from coco.names file
        self.classes = []

        try :
            # Read class names from coco.names file
            with open('../model/coco.names', 'r') as f :
                self.classes = f.read().splitlines()

        except IOError as e :
            # Log an error if reading coco.names file fails
            self.logger.error("Failed to read coco.names file: %s", str(e))

        # Initialize an empty list to store detected objects
        self.detected_objects = []

    def detect_objects(self, image_path) :
        """
            Detects objects in an image using YOLO model.

            Args:
                image_path (str): The path to the image file.

            Returns:
                list: List of detected objects, each represented by a tuple of class label and bounding box coordinates.
        """
        try :
            # Load the image and preprocess it for YOLO
            image = cv2.imread(image_path)
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.get_output_layers())

        except (cv2.error, IOError) as e :
            # Log an error if image processing or forward pass fails
            self.logger.error("Failed to process image or forward pass: %s", str(e))
            return []

        class_ids = []
        confidences = []
        boxes = []

        try :
            # Extract detected objects' information
            for out in outs :
                for detection in out :
                    scores = detection[5 :]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 :
                        center_x = int(detection[0] * image.shape[1])
                        center_y = int(detection[1] * image.shape[0])
                        w = int(detection[2] * image.shape[1])
                        h = int(detection[3] * image.shape[0])
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

        except IndexError as e :
            # Log an error if processing detections fails
            self.logger.error("Failed to process detections: %s", str(e))
            return []

        try :
            # Apply Non-Maximum Suppression to filter out redundant detections
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
            detected_objects = []
            for i in range(len(boxes)) :
                if i in indexes :
                    label = str(self.classes[class_ids[i]])
                    detected_objects.append((label, boxes[i]))
            return detected_objects

        except cv2.error as e :
            # Log an error if NMS or processing detected objects fails
            self.logger.error("Failed to perform NMS or process detected objects: %s", str(e))
            return []

    def get_output_layers(self) :
        """
            Retrieves the names of the output layers of the YOLO model.

            Returns:
                list: List of output layer names.
        """
        try :
            # Get output layers' names for YOLO
            layers_names = self.net.getLayerNames()
            unconnected_layers = self.net.getUnconnectedOutLayers()
            output_layers = [layers_names[layer - 1] for layer in unconnected_layers]
            return output_layers

        except (cv2.error, IndexError) as e :
            # Log an error if getting output layers fails
            self.logger.error("Failed to get output layers: %s", str(e))
            return []
