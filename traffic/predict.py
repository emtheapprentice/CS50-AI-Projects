import tensorflow as tf
import cv2
import numpy as np
import sys
import os

if len(sys.argv) != 2:
    sys.exit("Usage: python predict.py model")

model = tf.keras.models.load_model(sys.argv[1])

path = os.path.join
src = cv2.imread('gtsrb/gtsrb/22/00000_00000.ppm', cv2.IMREAD_UNCHANGED)
size = (30, 30)
resized = cv2.resize(src, size, interpolation = cv2.INTER_AREA)

prediction = model.predict(resized.reshape(1, 30, 30, 3)).argmax()
print('Traffic sign of type', prediction)