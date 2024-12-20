import cv2
from object_detector import *
import numpy as np

# Cargar el Detector de Aruco
parametros = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.Dictionary(cv2.aruco.DICT_5X5_50,1)


# Cargar el Detector de Objetos
detector = HomogeneousBgDetector()

# Cargar imagen
img = cv2.imread("images/22.jpg")

# Detectar el Marcador Aruco
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parametros)

# Dibujar un polígono alrededor del marcador
int_corners = np.int0(corners)
cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

# Calcular el perímetro del marcador Aruco
aruco_perimeter = cv2.arcLength(corners[0], True)

# Calcular la Relación de Píxeles a Centímetros
pixel_cm_ratio = aruco_perimeter / 20

#Detectar Objetos en la imagen
contours = detector.detect_objects(img)

# Dibujar los contornos de los objetos y mostrar sus dimensiones
for contorno in contours:
    # Obtener el rectángulo mínimo que encierra el contorno
    rect = cv2.minAreaRect(contorno)
    (x, y), (w, h), angle = rect

    #Calcular el ancho y la altura de los objetos aplicando la relación píxel a cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio

    #Mostrar el rectángulo
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 2)
    cv2.putText(img, "Ancho {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
    cv2.putText(img, "Alto {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)



cv2.imshow("Imagen", img)
cv2.waitKey(0)