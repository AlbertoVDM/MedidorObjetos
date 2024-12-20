import cv2
from object_detector import *
import numpy as np

#Cargar el Detector de Aruco
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

#Cargar el Detector de Objetos
detector = HomogeneousBgDetector()

#Configurar la Cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, img = cap.read()

    # Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    if corners:

        #Dibujar el polígono alrededor del marcador Aruco y calcular la relación de píxeles a cm
        int_corners = np.intp(corners)
        cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 20

        #Detección de objetos en la imagen
        contours = detector.detect_objects(img)

        #Detección de objetos en la imagen
        for contorno in contours:

            rect = cv2.minAreaRect(contorno)
            (x, y), (w, h), angle = rect

            # Obtener el ancho y el alto de los objetos aplicando la relación de píxeles a cm
            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            #Mostrar rectangulo
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.polylines(img, [box], True, (255, 0, 0), 2)
            cv2.putText(img, "Ancho {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
            cv2.putText(img, "Alto {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
    else:
        print("Marcador aruco no detectado")

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
