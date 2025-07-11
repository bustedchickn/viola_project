import pyvjoy
import time

j = pyvjoy.VJoyDevice(1)

print("Pressing Button 1 (Z)")
j.set_button(1, 1)
time.sleep(0.1)
j.set_button(1, 0)

time.sleep(1)

print("Pressing Button 2 (X)")
j.set_button(2, 1)
time.sleep(0.1)
j.set_button(2, 0)

time.sleep(1)

print("Pressing Button 3 (C)")
j.set_button(3, 1)
time.sleep(0.1)
j.set_button(3, 0)
