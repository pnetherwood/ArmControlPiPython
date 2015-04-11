# Python Script for controlling Robot Arm and Motor on Raspberry PI
Python scripts running on Raspberry PI for arm/robot control. These Python scripts run a socket server to control the Maplin robot arm annd the Ryanteck motor controller. arm_server.py listens for socket connections on port 5000.


Maplin Robot Arm: http://www.maplin.co.uk/p/robotic-arm-kit-with-usb-pc-interface-a37jn
Ryanteck Motor Controller: http://www.ryanteck.uk/store/ryanteck-rpi-motor-controller-board

Dependencies
============
PyUSB https://pypi.python.org/pypi/pyusb

Arm control based on original article in MagPi Issue 3: http://www.themagpi.com/issue/issue-3/article/skutter-write-a-program-for-usb-device

Running the Server
==================

To start the server:

  $ sudo python arm_server.py
  
Server will wait for commands send from Android app. See https://github.com/pnetherwood/ArmControlAndroid

Auto run server by adding the following to /etc/rc.local

  python /home/pi/arm/arm_server.py &
  
To make it easier to find and connect to server, setup a static IP address for the Raspberry Pi. See http://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address
