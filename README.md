# RobotArmControl
A Python script for controlling a robotic arm to unscrew a nut from a bolt and drop it on a nail.

## Overview
The Python script _armControlScript.py_ reads and executes the arm movement instructions provided in the _armInstructions.json_ file.
The current contents of _armInstructions.json_ are instructions for horizontally unscrewing of a nut from a bolt, moving the arm to vertically position the nut above a nail, and the dropping of the nut onto the nail.

This repository also includes the following additional materials:
- _RobotArmForwardAndInverseKinematics.nb_ is a Mathematica notebook including calculations for the forward and inverse kinematics of the arm.
- _robotArmReport.pdf_ is a report containing a detailed explanation of the task and further explanation of the inverse kinematics involved.
- _robotArm.ttt_ is a CoppeliaSim file containing a 3D model of the robot arm, bolt, and nail and simulation of the movement.

## Usage

### Dependencies
- [Adafruit ServoKit](https://docs.circuitpython.org/projects/servokit/en/latest/)

### Running
1. Connect to a Raspberry Pi wired to a 5-joint robot arm.
2. If desired, customize the instructions in _armInstructions.json_
3. Run _armControlScript.py_ to execute the instructions.
