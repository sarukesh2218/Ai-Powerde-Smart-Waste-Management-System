import serial
import time

esp32 = serial.Serial("COM12", 115200)
time.sleep(2)

esp32.write(b'P')
print("Sent Plastic command")

time.sleep(2)

esp32.write(b'O')
print("Sent Organic command")

time.sleep(2)

esp32.write(b'M')
print("Sent Metal command")

esp32.close()