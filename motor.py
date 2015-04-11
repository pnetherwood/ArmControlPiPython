import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

def forward():
        GPIO.output(17,1)
        GPIO.output(18,0)
        GPIO.output(22,1)
        GPIO.output(23,0)

def back():
        GPIO.output(17,0)
        GPIO.output(18,1)
        GPIO.output(22,0)
        GPIO.output(23,1)

def right():
        GPIO.output(17,0)
        GPIO.output(18,1)
        GPIO.output(22,1)
        GPIO.output(23,0)

def left():
        GPIO.output(17,1)
        GPIO.output(18,0)
        GPIO.output(22,0)
        GPIO.output(23,1)

def stop():
        GPIO.output(17,0)
        GPIO.output(18,0)
        GPIO.output(22,0)
        GPIO.output(23,0)

def setSpeed(s):
     pass

def cleanup():
        GPIO.cleanup()

if __name__ == "__main__":
    try:
       forward()
       while True:
          time.sleep(1)
    finally:
       print "Cleanup"
       stop()
       cleanup()

    
    
def test():    
    print "Left"
    left()
    time.sleep(2)
    stop()
    print "Right"
    right()
    time.sleep(2)
    stop()
    print "Forwards"
    forwards()
    time.sleep(2)
    stop()
    print "Backwards"
    back()
    time.sleep(2)
    stop()
    cleanup()
