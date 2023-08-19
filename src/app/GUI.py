import sqlite3
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

from src.app.EventDetection import EventDetection
from src.db.DatabaseManager import DatabaseManager


class EventDetectionUI :
    def __init__(self, root) :
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

    # Metoda pentru selectarea imaginii din sistemul de fișiere
    def select_image(self) :
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if self.image_path :
            self.image = cv2.imread(self.image_path)
            self.display_image()

    def detect_objects(self) :
        if self.image is not None :
            if self.image_path :
                detected_objects = self.backend.detect_objects(self.image_path)  # Trimiteți calea imaginii
                self.label_text.set("Detected Objects: " + ", ".join(detected_objects))
                self.db_manager.insert_detected_objects(detected_objects)
                self.display_image()

    def display_image(self) :
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (416, 416))
        img_pil = Image.fromarray(np.uint8(img))

        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk
