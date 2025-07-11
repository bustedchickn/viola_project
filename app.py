import aubio
import numpy as np
import sounddevice as sd
import time as Time
import keyboard as k
import pyvjoy
import threading
from pynput.keyboard import Controller, Key


keyboard = Controller()
samplerate = 44100
win_s = 4096
hop_s = 512
tolerance = 0.8
j = pyvjoy.VJoyDevice(1)


pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def button_press(btn):
    j.set_button(btn, 1)
    Time.sleep(.05)
    j.set_button(btn, 0)

last_time = 0
def audio_callback(indata, frames, time, status):
    global last_time
    samples = np.mean(indata, axis=1).astype(np.float32)
    pitch = pitch_o(samples)[0]
    now = Time.time()
    energy = np.sum(samples ** 2) / len(samples)
    if energy > 0.01:  # tweak this value!
        pitch = pitch_o(samples)[0]
    else:
        pitch = 0

    
    if pitch > 50:
        # print(f"Detected pitch: {pitch:.2f} Hz")
        # Example: map A4 (440Hz) to key "a"
        if 420 < pitch < 450:
            # a
            keyboard.press(Key.left)
        if not (420 < pitch < 450):
            keyboard.release(Key.left)

        if 285 < pitch < 300:
            # d
            keyboard.press(Key.right)
        if not (285 < pitch < 300):
            keyboard.release(Key.right)
        if 455 < pitch < 474:
            # w
            keyboard.press(Key.up)
        if not (455 < pitch < 474):
            keyboard.release(Key.up)
        if 385 < pitch < 403:
            # s
            keyboard.press(Key.down)
        if not (385 < pitch < 403):
            keyboard.release(Key.down)

        if 430*2 < pitch < 450*2 and now - last_time > 0.5:
            # a
            press_key(Key.left)
            last_time = now
            
        if 285*2 < pitch < 300*2 and now - last_time > 0.5:
            # d
            press_key(Key.right)
            last_time = now
        if 455*2 < pitch < 474*2 and now - last_time > 0.5:
            # w
            press_key(Key.up)
            last_time = now
        if 385*2 < pitch < 403*2 and now - last_time > 0.5:
            # s
            press_key(Key.down)
            last_time = now

        if 360 < pitch < 380 and now - last_time > 0.5:
            # z
            threading.Thread(target=button_press,args=(1,)).start()
            last_time = now
        if 320 < pitch < 340 and now - last_time > 0.5:
            # x
            threading.Thread(target=button_press,args=(2,)).start()
            last_time = now
        if 515 < pitch < 530 and now - last_time > 0.5:
            # c
            threading.Thread(target=button_press,args=(3,)).start()
            last_time = now

stream = sd.InputStream(channels=1, callback=audio_callback, samplerate=samplerate, blocksize=hop_s)
with stream:
    input("Press Enter to stop...\n")

