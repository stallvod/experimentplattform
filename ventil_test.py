import RPi.GPIO as GPIO
import time
from tkinter import *


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

def close_valve(seconds=0.05):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(17, GPIO.LOW)

def open_valve(seconds=0.05):
    GPIO.output(18, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(18, GPIO.LOW)

def open_pulse(seconds=1, pw=0.015):
    t = 0
    pulse = 0.1
    while t <= seconds:
        open_valve(pw)
        time.sleep(pulse - pw)
        t += pulse

def close_pulse(seconds=1, pw=0.015):
    t = 0
    pulse = 0.1
    while t <= seconds:
        close_valve(pw)
        time.sleep(pulse - pw)
        t += pulse        
    

root = Tk()
frame = Frame(root)
frame.pack()

Button(frame, text='Open', command=open_valve).pack()
Button(frame, text='Close', command=close_valve).pack()
Button(frame, text='Open 2s', command=lambda: open_pulse(1, 0.02)).pack()
Button(frame, text='Close 2s', command=lambda: close_pulse(1, 0.02)).pack()
    
mainloop()

GPIO.cleanup()
