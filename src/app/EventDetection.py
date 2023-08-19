import cv2
import numpy as np

class EventDetection :
    def __init__(self) :
        # Inițializarea detectorului YOLO
        self.net = cv2.dnn.readNet('../model/yolov3.cfg', '../model/yolov3.weights')
        self.classes = []
        with open('../model/coco.names', 'r') as f :
            # Încărcarea claselor de obiecte din fișierul coco.names
            self.classes = f.read().splitlines()

        self.detected_objects = []

    def detect_objects(self, image_path) :
        image = cv2.imread(image_path)

        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())

        class_ids = []
        confidences = []
        boxes = []

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

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)

        for i in range(len(boxes)) :
            if i in indexes :
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        detected_objects = []
        for i in range(len(boxes)) :
            if i in indexes :
                label = str(self.classes[class_ids[i]])
                print("Detected label:", label)  # Adăugați această linie pentru a verifica labelul detectat
                detected_objects.append(label)

        return detected_objects

    # Metoda pentru obținerea numelor stratelor de ieșire din rețea
    def get_output_layers(self) :
        layers_names = self.net.getLayerNames()
        print("Layers names:", layers_names)  # Print the layers names for debugging

        unconnected_layers = self.net.getUnconnectedOutLayers()
        print("Unconnected layers:", unconnected_layers)  # Print the unconnected layers for debugging

        output_layers = []
        for layer in unconnected_layers :
            output_layers.append(layers_names[layer - 1])
        print("Output layers:", output_layers)  # Print the calculated output layers for debugging

        return output_layers