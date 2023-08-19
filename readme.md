## Image Detection App

-------------------

Pentru a putea recunoaște obiectele în imagini și pentru a le eticheta cu tipurile corespunzătoare, puteți folosi un
model de învățare profundă preantrenat pentru detecția de obiecte, cum ar fi YOLO (You Only Look Once) sau SSD (Single
Shot MultiBox Detector). Aceste modele pot recunoaște și eticheta diferite tipuri de obiecte în imagini.

Pentru a face acest lucru, veți avea nevoie de o rețea neuronală convoluțională preantrenată pe un set de date mare care
să conțină diverse tipuri de obiecte. Modelul vă va furniza nu doar regiunile în care au fost detectate obiectele, ci și
etichetele corespunzătoare (cum ar fi "fruct", "mașină", "animal" etc.).

Voi exemplifica cum să utilizați YOLO cu ajutorul bibliotecii opencv-python pentru a detecta și eticheta obiectele
într-o imagine. Pentru a face acest lucru, aveți nevoie de fișierele YOLO preantrenate care definesc modelul și
etichetele.

Descărcați fișierele YOLO preantrenate și etichetele:

1. Descărcați fișierul yolov3.weights de la: https://pjreddie.com/media/files/yolov3.weights

2. Descărcați fișierul yolov3.cfg de la: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg

3. Descărcați fișierul coco.names de la: https://github.com/pjreddie/darknet/blob/master/data/coco.names