import socket
import sys
import arm
import time
from thread import *
#import motor as motor
import motorPWM as motor

def stop():
    print "stop"
    arm.stop()
    motor.stop()

def rotateBaseAC(on):
    print "rotateBaseAC: %s" % on
    if on:
        arm.moveBase(arm.rotateAC_cmd)
    else:
        arm.moveBase(0)

def rotateBaseCW(on):
    print "rotateBaseCW: %s" % on
    if on:
        arm.moveBase(arm.rotateCW_cmd)
    else:
        arm.moveBase(0)

def shoulderUp(on):
    print "shoulderUp: %s" % on
    if on:
        arm.moveShoulder(arm.shoulderUp_cmd)
    else:
        arm.moveShoulder(0)

def shoulderDown(on):
    print "shoulderDown: %s" % on
    if on:
        arm.moveShoulder(arm.shoulderDown_cmd)
    else:
        arm.moveShoulder(0)

def elbowUp(on):
    print "elbowUp: %s" % on
    if on:
        arm.moveElbow(arm.elbowUp_cmd)
    else:
        arm.moveElbow(0)

def elbowDown(on):
    print "elbowDown: %s" % on
    if on:
        arm.moveElbow(arm.elbowDown_cmd)
    else:
        arm.moveElbow(0)

def wristUp(on):
    print "wristUp: %s" % on
    if on:
        arm.moveWrist(arm.wristUp_cmd)
    else:
        arm.moveWrist(0)

def wristDown(on):
    print "wristDown: %s" % on
    if on:
        arm.moveWrist(arm.wristDown_cmd)
    else:
        arm.moveWrist(0)

def gripOpen(on):
    print "gripOpen: %s" % on
    if on:
        arm.moveGrip(arm.gripOpen_cmd)
    else:
        arm.moveGrip(0)

def gripClose(on):
    print "gripClose: %s" % on
    if on:
        arm.moveGrip(arm.gripClose_cmd)
    else:
        arm.moveGrip(0)

def lightOn(on):
    print "lightOn"
    arm.light(arm.lightOn_cmd)

def lightOff(on):
    print "lightOff"
    arm.light(arm.lightOff_cmd)

def forward(on):
    print "forward: %s" % on
    if on:
        motor.forward()
    else:
        motor.stop()

def back(on):
    print "back: %s" % on
    if on:
        motor.back()
    else:
        motor.stop()

def left(on):
    print "left: %s" % on
    if on:
        motor.left()
    else:
        motor.stop()

def right(on):
    print "right: %s" % on
    if on:
        motor.right()
    else:
        motor.stop()

def speed(s):
    print "speed: %s" % s
    motor.setSpeed(s)

# Set mapping between socket command name and function name
armoptions = {'BA' : rotateBaseAC,
              'BC' : rotateBaseCW,
              'SU' : shoulderUp,
              'SD' : shoulderDown,
              'EU' : elbowUp,
              'ED' : elbowDown,
              'WU' : wristUp,
              'WD' : wristDown,
              'GO' : gripOpen,
              'GC' : gripClose,
              'LO' : lightOn,
              'LF' : lightOff,
              'FF' : forward,
              'BB' : back,
              'LL' : left,
              'RR' : right,
              'SS' : speed}


HOST = '' # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow socket reuse
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST,PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)

def clientthread(conn):
    # Keep running until quit command executed
    while 1:
        # Get the data
        data = conn.recv(1024)

        if not data:
            print "Socket closed"
            break

        # Strip off any whitespace if present
        data = ''.join(data.split())

        # Loop through the recieved buffer a character at a time building up commands
        i = 0;
        cmd = ""
        while i < len(data):
            # Look for the special case of arm stop
            if data[i] == '.':
                stop()
                i += 1
                continue

            # Build up command
            cmd += data[i]

            # If enough characters for a command has been found then interpret and call function
            if len(cmd) == 2:
                param = True
                if len(data) > i+1:
                    # on/off cmd
                    if data[i+1] == '+':
                        param = True
                        i += 1
                    elif data[i+1] == '-':
                        param = False
                        i += 1
                    elif data[i+1].isdigit():
                        param = data[i+1]
                        i += 1

                # Get option and call function
                try:
                    armoptions[cmd](param)
                except KeyError:
                    print "Bad command: " + cmd

                # Clear command once issued
                cmd = ""

            # Move onto next character
            i += 1


##
## Main starting piont of server
## 
running = True
try:
    while running:
        print "Waiting ..."
        # Wait to accept a connection from client control app
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])

        # Start listening to new socket on seperate thread
        start_new_thread(clientthread ,(conn,))
  
finally:
    print "Exiting"
    try:
        arm.stop()  # Stop the arm if we get here in error
    except:
        pass
    s.close()
    time.sleep(0.1) # wait a little for threads to finish
    motor.cleanup()

