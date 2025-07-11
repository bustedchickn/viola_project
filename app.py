import aubio
import numpy as np
import sounddevice as sd
from pynput.keyboard import Controller, Key

keyboard = Controller()
samplerate = 44100
win_s = 4096
hop_s = 512
tolerance = 0.8

pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(tolerance)

def audio_callback(indata, frames, time, status):
    samples = np.mean(indata, axis=1).astype(np.float32)
    pitch = pitch_o(samples)[0]
    if pitch > 50:
        # print(f"Detected pitch: {pitch:.2f} Hz")
        # Example: map A4 (440Hz) to key "a"
        if 430 < pitch < 450:
            # a
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        if 285 < pitch < 300:
            # d
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        if 455 < pitch < 474:
            # w
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        if 385 < pitch < 403:
            # s
            keyboard.press(Key.down)
            keyboard.release(Key.down)

stream = sd.InputStream(channels=1, callback=audio_callback, samplerate=samplerate, blocksize=hop_s)
with stream:
    input("Press Enter to stop...\n")

