#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
shoulder = Motor(Ports.PORT1, True)
limit_switch_lower = Limit(brain.three_wire_port.a)
encoder_bicep = Encoder(brain.three_wire_port.c)
ptmr = Potentiometer(brain.three_wire_port.h)
elbow = Motor(Ports.PORT5, False)
claw = Servo(brain.three_wire_port.b)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
import math
#import numpy as np

# Begin project code



def Calibrate():
    #speed up velocities
    shoulder.set_velocity(100, PERCENT)
    elbow.set_velocity(70, PERCENT)

    #angle at which shoulder motor hits limit switch
    calibration_angle = 5

    while(ptmr.angle(DEGREES) < 160): # was 200
        elbow.spin(FORWARD)
    elbow.stop()

    while(not limit_switch_lower.pressing()):
        shoulder.spin(FORWARD)
        

    print("-------- PRESSING ----------")
    encoder_bicep.set_position(calibration_angle,DEGREES)
    shoulder.stop()
    
    #reset velocities
    shoulder.set_velocity(70, PERCENT)
    elbow.set_velocity(50, PERCENT)

def forwardKin(shoulderA, elbowA):
    print("forwardKin called with", shoulderA, ",", elbowA)

    shoulderARadians = math.radians(shoulderA)
    x = bicep_length * math.cos(shoulderARadians)
    y = bicep_length * math.sin(shoulderARadians)

    elbowLocation = (x,y)

#which direction is theta increasing?
#where are you measuring your angle 0 from

    # forward kinematics

    alpha = math.pi - shoulderA - elbowA
    alpha = math.radians(alpha)

    x2 = x - forearm_length * math.cos(alpha)
    y2 = y + forearm_length * math.sin(alpha)

    tipLocation = (x2,y2)

    print("tip: " + str(tipLocation))
    return tipLocation

def goto(shoulderA, elbowA, skipSafety):
    print("goTo called with", shoulderA, ",", elbowA)
    # elbow angles 80 < x < 200
    # shoulder angles 3 < x < 102
    
    # stop motors
    shoulder.stop()
    elbow.stop()

    # project tip location with forward kinematics
    projTipLocation = forwardKin(shoulderA, elbowA)

    print("proj x: ", projTipLocation[0])
    print("proj y: ", projTipLocation[1])

    #if((projTipLocation[0] < 10 and projTipLocation[1] > 1) or (projTipLocation[0] > 10 and projTipLocation[1] < 5)): 

    # safety checks
    if(((projTipLocation[0] < 10 and projTipLocation[1] < 5) or projTipLocation[1] < 0)) and not skipSafety:
        # angles are unsafe to go to
        print("GoTo will hit something")
    else:
        # angles are safe to go to
        print("GoTo validated")
        while encoder_bicep.position(DEGREES) < shoulderA:
            shoulder.spin(REVERSE)
            wait(0.1,SECONDS)
            print("enc angle: ", encoder_bicep.position(DEGREES))
        shoulder.stop()

        while ptmr.angle(DEGREES) + ptmr_offset > elbowA:
            elbow.spin(REVERSE)
            wait(0.1,SECONDS)
            print("ptmr angle: ", ptmr.angle(DEGREES) + ptmr_offset )
        elbow.stop()    


def invKin(x, y):
    print("invKin called with", x, ",", y)
    #given a desired coordinate pair, calculates the angles
    #necessary to send the claw to that location

    #side lengths a and b are constant    
    l1 = bicep_length
    l2 = forearm_length

    ##Solve for theta2
    cos_theta2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    theta2 = math.acos(cos_theta2)
    theta2 = math.degrees(theta2)

    ##Solve for theta1
    alpha = math.atan(y / x)

    theta1_numerator = l2  * math.sin(theta2)
    theta1_denominator = math.sqrt(x**2 + y**2)
    theta1_fraction = theta1_numerator / theta1_denominator
    theta1 = alpha - math.asin( theta1_fraction )

    theta1 = math.degrees(theta1)

    print("theta1: ", theta1)
    print("theta2: ", theta2)

    angles = (theta1, theta2)
    return angles

#--------------------------------------------------
#MAIN
#--------------------------------------------------

# set constants
bicep_length = 9.75
forearm_length = 10.55
ptmr_offset = -30 #deg
wait(0.1,SECONDS)

#claw.set_position(-50,DEGREES) open
#wait(1, SECONDS)
#claw.set_position(100,DEGREES) close

Calibrate()

#safe test
#goto(60, 90, True)
#wait(10, SECONDS)

anglesTuple = invKin(15, 10)
goto(anglesTuple[0],anglesTuple[1] + 60, True)
#goto(68, 54, True)

#--------------------------------------------------
    



        
 
