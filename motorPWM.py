# ROBOT TANK MOTOR CONTROL
#
# Uses Ryanteck board
#

import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
motor1F = 17
motor1B = 18
motor2F = 22
motor2B = 23
GPIO.setup(motor1F,GPIO.OUT)
GPIO.setup(motor1B,GPIO.OUT)
GPIO.setup(motor2F,GPIO.OUT)
GPIO.setup(motor2B,GPIO.OUT)

# Setup globals
frequency = 250
motor1F_PWM = GPIO.PWM(motor1F,frequency)
motor1B_PWM = GPIO.PWM(motor1B,frequency)
motor2F_PWM = GPIO.PWM(motor2F,frequency)
motor2B_PWM = GPIO.PWM(motor2B,frequency)
dutyCycle = 65
minSpeed = 40

def setSpeed(s):
    global dutyCycle
    dutyCycle = (float(s)-1)*((100-minSpeed)/8) + minSpeed;


def forward():
    motor1B_PWM.stop()
    motor2B_PWM.stop()
    motor1F_PWM.start(dutyCycle)
    motor2F_PWM.start(dutyCycle)

def back():
    motor1F_PWM.stop()
    motor2F_PWM.stop()
    motor1B_PWM.start(dutyCycle)
    motor2B_PWM.start(dutyCycle)

def right():
    motor1F_PWM.stop()
    motor2B_PWM.stop()
    motor1B_PWM.start(dutyCycle)
    motor2F_PWM.start(dutyCycle)

def left():
    motor1B_PWM.stop()
    motor2F_PWM.stop()
    motor1F_PWM.start(dutyCycle)
    motor2B_PWM.start(dutyCycle)
    
def stop():
    motor1B_PWM.stop()
    motor2B_PWM.stop()
    motor1F_PWM.stop()
    motor2F_PWM.stop()

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

