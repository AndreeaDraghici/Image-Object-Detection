import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

from src.app.EventDetection import EventDetection
from src.db.DatabaseManager import DatabaseManager

class EventDetectionUI :
    def __init__(self, root) :
        # Inițializarea ferestrei principale
        self.root = root
        self.root.title("Object Detection Application")

        # Dezactivează redimensionarea ferestrei
        self.root.resizable(False, False)

        self.backend = EventDetection()
        self.db_manager = DatabaseManager()

        # Inițializarea calei imaginii și a imaginii încărcate
        self.image_path = ""
        self.image = None

        # Inițializarea canvasului pentru afișarea imaginii
        self.canvas = tk.Canvas(root, width=416, height=416)
        self.canvas.pack()

        # Inițializarea butonului pentru selectarea imaginii
        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack()

        # Inițializarea butonului pentru detectarea obiectelor
        self.detect_button = tk.Button(root, text="Detect Objects", command=self.detect_objects)
        self.detect_button.pack()

        # Inițializarea etichetei pentru afișarea tipurilor de obiecte detectate
        self.label_text = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.label_text)
        self.label.pack()

    # Metoda pentru selectarea imaginii din sistemul de fișiere
    def select_image(self) :
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        if self.image_path :
            print("Selected image path:", self.image_path)  # Afișează calea imaginii
            self.image = cv2.imread(self.image_path)

            if self.image is not None :
                print("Image loaded successfully.")
                self.display_image()
            else :
                print("Failed to load image.")

    def detect_objects(self) :
        if self.image is not None :
            if self.image_path :
                detected_objects = self.backend.detect_objects(self.image_path)  # Trimiteți calea imaginii

                print("Image path: ", self.image_path)
                print("Detected objects: ", detected_objects)

                self.label_text.set("Detected Objects: Detecting...")  # Setează un text temporar

                # Aplică suprimarea non-maximelor pentru a elimina detecțiile redundante
                unique_detected_objects = list(set(detected_objects))

                self.db_manager.insert_detected_objects(unique_detected_objects)
                self.display_image()

                # Actualizează etichetele și lista de obiecte detectate
                self.update_detected_objects(unique_detected_objects)

                # Actualizează etichetele și lista de obiecte după un anumit interval de timp
                self.root.after(5, self.update_detected_objects, unique_detected_objects)

    def update_detected_objects(self, detected_objects) :
        self.label_text.set("Detected Objects: " + ", ".join(detected_objects))
        self.root.update()  # Actualizați interfața grafică pentru a reflecta noile etichete

    def display_image(self) :
        if self.image is None :
            print("Image not loaded!")
            return

        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (416, 416))
        img_pil = Image.fromarray(np.uint8(img))

        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk
