#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
bicep_motor = Motor(Ports.PORT1, True)
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

# Begin project code



def Calibrate():
    bicep_motor.set_velocity(70, PERCENT)
    calibration_angle = 5

    while(ptmr.angle(DEGREES) < 180): # was 200
        elbow.spin(FORWARD)
    elbow.stop()

    while(not limit_switch_lower.pressing()):
        bicep_motor.spin(FORWARD)
        

    print("-------- PRESSING ----------")
    encoder_bicep.set_position(calibration_angle,DEGREES)
    bicep_motor.stop()


def forwardKin(shoulderA, elbowA):
    
    shoulderARadians = math.radians(shoulderA)
    x = bicep_length * math.cos(shoulderARadians)
    y = bicep_length * math.sin(shoulderARadians)

    elbowLocation = (x,y)

    # forward kinematics

    alpha = math.pi - shoulderA - elbowA
    alpha = math.radians(alpha)

    x2 = x - forearm_length * math.cos(alpha)
    y2 = y + forearm_length * math.sin(alpha)

    tipLocation = (x2,y2)

    print("tip: " + str(tipLocation))
    return tipLocation


def goto(shoulderA, elbowA):
    # elbow angles 80 < x < 200
    # shoulder angles 3 < x < 102
    
    # stop motors
    bicep_motor.stop()
    elbow.stop()

    # project tip location with forward kinematics
    projTipLocation = forwardKin(shoulderA, elbowA)

    print("proj x: ", projTipLocation[0])
    print("proj y: ", projTipLocation[1])

    #if((projTipLocation[0] < 10 and projTipLocation[1] > 1) or (projTipLocation[0] > 10 and projTipLocation[1] < 5)): 

    # safety checks
    if((projTipLocation[0] < 10 and projTipLocation[1] < 5) or projTipLocation[1] < 0):
        # angles are unsafe to go to
        print("GoTo will hit something")
    else:
        # angles are safe to go to
        print("GoTo validated")
        while encoder_bicep.position(DEGREES) < shoulderA:
            bicep_motor.spin(REVERSE)
        bicep_motor.stop()

        while ptmr.angle(DEGREES) > elbowA:
            elbow.spin(REVERSE)
        elbow.stop()    


def invKin(x, y,l1,l2):
    #side lengths a and b are constant
    #bicep_length
    #forearm_length

    ##Solve for theta2
    theta2_fraction = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    theta2 = math.acos(theta2_fraction)

    ##Solve for theta1
    alpha = math.atan(y / x)

    theta1_numerator = l2  * math.sin(theta2)
    theta1_denominator = math.sqrt(x**2 + y**2)
    theta1_fraction = theta1_denominator / theta1_arcsinFraction
    theta1_arcsin = math.asin( theta1_fraction )

    theta1 = alpha + theta1_arcsin

    pass

#--------------------------------------------------
#MAIN
#--------------------------------------------------

# set constants
encoder_offset = 10
bicep_length = 9.75
forearm_length = 10.55
wait(0.1,SECONDS)

#claw.set_position(-50,DEGREES) open
#wait(1, SECONDS)
#claw.set_position(100,DEGREES) close

Calibrate()

#safe test
goto(60, 90)

#unsafe test due to hitting gearbox
goto(60, 60)


#unsafe test due to hitting table
goto(45, 45)


#--------------------------------------------------
#archive

#print("angle:  " + str(encoder_angle))
#print("adjusted angle: " + str(encoder_angle + encoder_offset))

#while(True):
#    current_angle = encoder_bicep.position(DEGREES)
#    bicep_motor.spin(REVERSE)
#    print(ptmr.angle(DEGREES))
#    print(encoder_bicep.position(DEGREES))
#    wait(0.25,SECONDS)
#    forwardKin(bicep_length,current_angle + encoder_offset)
    



        
