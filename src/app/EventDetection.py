import logging

import cv2
import numpy as np

from src.LoadLoggingConfig import load_logging_config


class EventDetection :

    def __init__(self) :
        load_logging_config()
        self.logger = logging.getLogger('development')

        try :
            # Initialize the YOLO detector
            self.net = cv2.dnn.readNet('../model/yolov3.cfg', '../model/yolov3.weights')
        except cv2.error as e :
            self.logger.error("Failed to initialize YOLO detector: %s", str(e))

        self.classes = []
        try :
            with open('../model/coco.names', 'r') as f :
                self.classes = f.read().splitlines()
        except IOError as e :
            self.logger.error("Failed to read coco.names file: %s", str(e))

        self.detected_objects = []

    def detect_objects(self, image_path) :
        try :
            image = cv2.imread(image_path)
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.get_output_layers())
        except (cv2.error, IOError) as e :
            self.logger.error("Failed to process image or forward pass: %s", str(e))
            return []

        class_ids = []
        confidences = []
        boxes = []

        try :
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
            self.logger.error("Failed to process detections: %s", str(e))
            return []

        try :
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
            detected_objects = []
            for i in range(len(boxes)) :
                if i in indexes :
                    label = str(self.classes[class_ids[i]])
                    detected_objects.append((label, boxes[i]))
            return detected_objects
        except cv2.error as e :
            self.logger.error("Failed to perform NMS or process detected objects: %s", str(e))
            return []

    def get_output_layers(self) :
        try :
            layers_names = self.net.getLayerNames()
            unconnected_layers = self.net.getUnconnectedOutLayers()
            output_layers = [layers_names[layer - 1] for layer in unconnected_layers]
            return output_layers
        except (cv2.error, IndexError) as e :
            self.logger.error("Failed to get output layers: %s", str(e))
            return []
