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
            # Open the 'coco.names' file containing class names
            with open('../model/coco.names', 'r') as f :
                # Read the contents of the file and split lines into a list
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
            # Load the image using OpenCV and preprocess it for YOLO
            image = cv2.imread(image_path)
            # Preprocess the image for input to the neural network
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            # Set the preprocessed image as input to the YOLO neural network
            self.net.setInput(blob)
            # Perform forward pass through the network to get detection results
            outs = self.net.forward(self.get_output_layers())
        except (cv2.error, IOError) as e :
            # Log an error if image processing or forward pass fails
            self.logger.error("Failed to process image or forward pass: %s", str(e))
            return []

        # Initialize empty lists to store information about detected objects
        class_ids = []  # List to store the IDs of detected object classes
        confidences = []  # List to store the confidence scores of detected objects
        boxes = []  # List to store the coordinates of bounding boxes for detected objects

        try :
            # Extract detected objects' information
            for out in outs :
                # Iterate through each detection in the current result
                for detection in out :
                    # Extract confidence scores for object classes
                    scores = detection[5 :]
                    # Get the index of the class with the highest score
                    class_id = np.argmax(scores)
                    # Get the confidence score of the detected class
                    confidence = scores[class_id]
                    # Check if the confidence score is above the threshold (0.5)
                    if confidence > 0.5 :
                        # Calculate object center coordinates, width, and height
                        center_x = int(detection[0] * image.shape[1])
                        center_y = int(detection[1] * image.shape[0])
                        w = int(detection[2] * image.shape[1])
                        h = int(detection[3] * image.shape[0])

                        # Calculate top-left corner coordinates of the bounding box
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        # Store class ID, confidence, and bounding box coordinates
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])
        except IndexError as e :
            # Log an error if processing detections fails
            self.logger.error("Failed to process detections: %s", str(e))
            return []

        try :
            # Perform Non-Maximum Suppression to filter out overlapping bounding boxes
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
            # Create an empty list to store detected objects
            detected_objects = []

            # Iterate through all bounding boxes
            for i in range(len(boxes)) :
                # Check if the current box survived NMS
                if i in indexes :
                    # Get the label corresponding to the class ID from the classes list
                    label = str(self.classes[class_ids[i]])

                    # Append the label and bounding box coordinates to the list of detected objects
                    detected_objects.append((label, boxes[i]))

            # Return the list of detected objects after NMS
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
            # Get the names of the output layers from the YOLO network
            layers_names = self.net.getLayerNames()

            # Get the indices of the unconnected output layers
            unconnected_layers = self.net.getUnconnectedOutLayers()

            # Create a list of output layer names by subtracting 1 from each index
            output_layers = []
            for layer in unconnected_layers :
                output_layers.append(layers_names[layer - 1])

            # Return the list of output layer names
            return output_layers
        except (cv2.error, IndexError) as e :
            # Log an error if getting output layers fails
            self.logger.error("Failed to get output layers: %s", str(e))
            return []