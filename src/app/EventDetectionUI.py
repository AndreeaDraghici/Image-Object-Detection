import logging
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

from src.LoadLoggingConfig import load_logging_config
from src.app.EventDetection import EventDetection
from src.db.DatabaseManager import DatabaseManager


class EventDetectionUI :
    def __init__(self, root) :
        try :
            load_logging_config()
            self.logger = logging.getLogger('EventDetectionUI')

            self.root = root
            self.root.title("Object Detection Application")
            self.root.resizable(False, False)

            self.backend = EventDetection()
            self.db_manager = DatabaseManager()

            self.image_path = ""
            self.image = None

            self.canvas = tk.Canvas(root, width=416, height=416)
            self.canvas.pack()

            self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
            self.select_button.pack()

            self.detect_button = tk.Button(root, text="Detect Objects", command=self.detect_objects)
            self.detect_button.pack()

            self.label_text = tk.StringVar()
            self.label = tk.Label(root, textvariable=self.label_text)
            self.label.pack()
        except Exception as e :
            self.logger.error("An error occurred during UI initialization: %s", str(e))

    def select_image(self) :
        try :
            self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

            if self.image_path :
                self.logger.info("Selected image path: " + self.image_path)
                self.image = cv2.imread(self.image_path)

                if self.image is not None :
                    self.logger.info("Image loaded successfully.")
                    self.display_image()
                else :
                    RuntimeError("Failed to load image.")
                    return
        except Exception as e :
            self.logger.error("An error occurred during image selection: %s", str(e))

    def detect_objects(self) :
        try :
            if self.image is not None and self.image_path :
                if self.image_path :
                    detected_objects = self.backend.detect_objects(self.image_path)
                    self.logger.info("Image path: " + self.image_path)
                    self.logger.info("Detected objects: " + str(detected_objects))

                    self.label_text.set("Detected Objects: Detecting...")

                    unique_detected_objects = []
                    for obj_label, _ in detected_objects :
                        unique_detected_objects.append(obj_label)

                    self.db_manager.insert_detected_objects(detected_objects)
                    self.display_image()
                    self.update_detected_objects(unique_detected_objects)
                    self.root.after(5, self.update_detected_objects, unique_detected_objects)
        except Exception as e :
            self.logger.error("An error occurred during object detection: %s", str(e))

    ''' 
    def display_selected_object(self, obj_label) :
        if self.image is not None and self.image_path :
            detected_objects = self.backend.detect_objects(self.image_path)

            for obj_label_detected, coords in detected_objects :
                if obj_label_detected == obj_label :
                    x, y, w, h = coords
                    selected_img = self.image.copy()

                    # Redimensionați imaginea pentru afișarea etichetei
                    selected_img = cv2.resize(selected_img, (416, 416))

                    # Ajustați coordonatele obiectului pentru imaginea redimensionată
                    x = int(x * 416 / self.image.shape[1])
                    y = int(y * 416 / self.image.shape[0])
                    w = int(w * 416 / self.image.shape[1])
                    h = int(h * 416 / self.image.shape[0])

                    # Desenează un chenar în jurul obiectului și afișează eticheta
                    cv2.rectangle(selected_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label_position = (x, y + h + 20)  # Ajustați poziția etichetei
                    cv2.putText(selected_img, obj_label, label_position, cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)

                    img_pil = Image.fromarray(np.uint8(selected_img))
                    img_tk = ImageTk.PhotoImage(image=img_pil)

                    self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                    self.canvas.image = img_tk
                    break
    '''

    def display_image(self) :
        try :
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (416, 416))
            detected_objects = self.backend.detect_objects(self.image_path)

            for obj_label, coords in detected_objects :

                x, y, w, h = coords

                # Ajustați coordonatele obiectului pentru imaginea redimensionată
                x = int(x * 416 / self.image.shape[1])
                y = int(y * 416 / self.image.shape[0])
                w = int(w * 416 / self.image.shape[1])
                h = int(h * 416 / self.image.shape[0])

                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                label_position = (x, y + h + 20)
                cv2.putText(img, obj_label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                img_pil = Image.fromarray(np.uint8(img))
                img_tk = ImageTk.PhotoImage(image=img_pil)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
                self.canvas.image = img_tk

                if self.image is None :
                    RuntimeError("Image not loaded!")
                    return

        except Exception as e :
            self.logger.error("An error occurred during image display: %s", str(e))

    def update_detected_objects(self, detected_objects) :
        try :
            self.label_text.set("Detected Objects: " + ", ".join(detected_objects))
            self.root.update()
        except Exception as e :
            self.logger.error("An error occurred during updating detected objects: %s", str(e))
