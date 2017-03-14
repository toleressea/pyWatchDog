import time
import audiere

def playTone(frequency, duration):
    d = audiere.open_device()
    t = d.create_tone(frequency)
    t.play()
    time.sleep(duration)
    t.stop()
