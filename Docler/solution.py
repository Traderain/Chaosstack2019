import cv2
import base64
import numpy as np

f = open("asd.txt", "r")
origimg = f.readline()

def data_uri_to_cv2_img(encoded_data):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

img = data_uri_to_cv2_img(origimg)
cv2.imwrite('h.png', img)
