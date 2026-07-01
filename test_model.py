import serial
import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model

esp32 = serial.Serial("COM12", 115200)
time.sleep(3)

model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").read().splitlines()

camera = cv2.VideoCapture(1)

while True:
    ret, image = camera.read()
    if not ret:
        break

    resized = cv2.resize(image, (224, 224))
    input_image = np.asarray(resized, dtype=np.float32)
    input_image = (input_image / 127.5) - 1
    input_image = np.expand_dims(input_image, axis=0)

    prediction = model.predict(input_image, verbose=0)
    index = np.argmax(prediction)
    label = class_names[index].strip().lower()
    confidence = prediction[0][index]

    cv2.putText(image, f"AI: {label} {confidence:.2f}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.putText(image, "Press P/O/M",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 255), 2)

    cv2.imshow("Smart Waste", image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('p'):
        esp32.write(b'P')
    elif key == ord('o'):
        esp32.write(b'O')
    elif key == ord('m'):
        esp32.write(b'M')
    elif key == ord('q'):
        break

camera.release()
esp32.close()
cv2.destroyAllWindows()