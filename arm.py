# ROBOT ARM CONTROL PROGRAM

# import the USB and Time libraries into Python
import usb.core, usb.util, time

RoboArm = None
print "Searching for robot arm ..."
while RoboArm is None:
    # Allocate the name 'RoboArm' to the USB device
    RoboArm = usb.core.find(idVendor=0x1267,idProduct =0x0000)
    time.sleep(1)
print "Arm found."


# Define a procedure to execute each movement
def MoveArm(duration, armCmd):
    if RoboArm is None:
        return
    # Start the movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,armCmd, 1000)

    # Sleep foer the given duration, otherwise arm will keep moving
    if duration!=0:
        # Stop movement after waiting specified time
        time.sleep(duration)
        armCmd=[0,0,0]
        RoboArm.ctrl_transfer(0x40,6,0x100,0,armCmd, 1000)

# Define the commands for each motor
rotateAC_cmd=1 # Rotate Base Anti-clockwise
rotateCW_cmd=2 # Rotate Base Clockwise
shoulderUp_cmd=64 # Shoulder Up
shoulderDown_cmd=128 # Shoulder Down
elbowUp_cmd=16 # Elbow Up
elbowDown_cmd=32 # Elbow Down
wristUp_cmd=4 # Wrist Up
wristDown_cmd=8 # Wrist Down
gripOpen_cmd=2 # Grip Open
gripClose_cmd=1 # Grip Close
lightOn_cmd=1 # Light On
lightOff_cmd=0 # Light Off
stop_cmd=[0,0,0]

# Global variables that holds the current state of the arm
shoulderState=0
wristState=0
elbowState=0
gripState=0
baseState=0
lightState=0

def moveBase(base_cmd):
    updateArmState(shoulderState, wristState, elbowState, gripState, base_cmd, lightState)

def moveWrist(wrist_cmd):
    updateArmState(shoulderState, wrist_cmd, elbowState, gripState, baseState, lightState)

def moveShoulder(shoulder_cmd):
    updateArmState(shoulder_cmd, wristState, elbowState, gripState, baseState, lightState)

def moveElbow(elbow_cmd):
    updateArmState(shoulderState, wristState, elbow_cmd, gripState, baseState, lightState)

def moveGrip(grip_cmd):
    updateArmState(shoulderState, wristState, elbowState, grip_cmd, baseState, lightState)

def light(light_cmd):
    updateArmState(shoulderState, wristState, elbowState, gripState, baseState, light_cmd)

# Use the state to update which motors should be driving
def updateArmState(shoulder, wrist, elbow, grip, base, light):
    global shoulderState, wristState, elbowState, gripState, baseState, lightState

    # Add the movement commands and create tuple to pass to usb
    armCommand=(shoulder + wrist + elbow + grip, base, light)

    # Tell the arm which motor to move
    RoboArm.ctrl_transfer(0x40,6,0x100,0,armCommand, 1000)

    # Update the state for next time
    shoulderState = shoulder
    wristState = wrist
    elbowState = elbow
    gripState = grip
    baseState = base
    lightState = light


# Stop all movement
def stop():       # Stop arm moving
    global shoulderState, wristState, elbowState, gripState, baseState, lightState
    RoboArm.ctrl_transfer(0x40,6,0x100,0,stop_cmd, 1000)
    shoulderState=0
    wristState=0
    elbowState=0
    gripState=0
    baseState=0
    lightState=0


if __name__ == "__main__":
    # Give the arm some test commands
    MoveArm(1,[0,1,0]) # Rotate Base Anti-clockwise
    MoveArm(1,[0,2,0]) # Rotate Base Clockwise
    MoveArm(1,[64,0,0]) # Shoulder Up
    MoveArm(1,[128,0,0]) # Shoulder Down
    MoveArm(1,[16,0,0]) # Elbow Up
    MoveArm(1,[32,0,0]) # Elbow Down
    MoveArm(1,[4,0,0]) # Wrist Up
    MoveArm(1,[8,0,0]) # Wrist Down
    MoveArm(1,[2,0,0]) # Grip Open
    MoveArm(1,[1,0,0]) # Grip Close
    MoveArm(1,[0,0,1]) # Light On
    MoveArm(1,[0,0,0]) # Light Off

