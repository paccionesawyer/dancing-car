'''
Tufts University, Spring 2020-2021
lineFollower3.py
By: Sawyer Bailey Paccione and Olif Hordofa
Completed: April 25th, 2021 10:30 PM

Description: Viennese Waltz Final Project 
'''
###############################################################################
#                                   Imports                                   #
###############################################################################
import hub 
import utime

###############################################################################
#                                  Initialize                                 #
###############################################################################
# Initialize Motor and Sensor Ports on Spike PRIME
motors          = hub.port.E.motor.pair(hub.port.B.motor)
follower        = hub.port.A.device
spinner         = hub.port.C.motor

spin_speed   = 27

# Raspberry Pi4 
serial = hub.port.D
serial.mode(hub.port.MODE_FULL_DUPLEX)
serial.baud(115200)

# Initialize Proportional Controller Values
PROPORTIONAL_GAIN   = 0.3  # k_p
Kd = 0.09
base_speed = 30

# Global Variables For PI Communication
curr = ""
next = ""
msg = "0"
    
motors.pwm(0,0)

###############################################################################
#                                  Main Code                                  #
###############################################################################
def trainLightSensors() :
    print("Training Light Sensors Now")
    lightSum = 0
    hub.display.show(str(0))
    for i in range(5) :
        while not hub.button.right.is_pressed():
            pass 
        hub.sound.beep()
        hub.display.show(str(i+1))
        light = follower.get()[0]
        lightSum += light
        while hub.button.right.is_pressed():
            pass

        
    lightVal = lightSum/5
    print()
    print("Light Value is:", lightVal)
    utime.sleep(1)
    
    hub.display.show(str(0))
    darkSum = 0
    for i in range(5) :
        while not hub.button.right.is_pressed():
            pass 
        hub.sound.beep()
        hub.display.show(str(i+1))
        dark = follower.get()[0]
        darkSum += dark
        while hub.button.right.is_pressed():
            pass
    
    darkVal = darkSum/5
    print()
    print("Dark Value is:", darkVal)
    utime.sleep(1)
    
    hub.display.show(hub.Image.YES)
    threshold = int((lightVal + darkVal) / 2)
    
    print("\n The threshold value is", threshold)
    utime.sleep(5)
    
    return threshold
    
def piMusicDetection(left, right):
    print("piMusic")
    try:
        #print("try")
        msg = serial.read(1)
        msg = str(msg.decode("UTF-8"))
        print(msg)
        #print("Msg Size:", len(msg))
        if hub.button.right.is_pressed():
            motors.pwm(0,0)
            
        if msg == "0" :
            spinner.pwm(0)
            #print("here0")
            # Music Is Off
            hub.display.show(hub.Image.NO)
            motors.pwm(0,0)
            
        elif msg == "1" :
            spinner.pwm(spin_speed)
            print("here1")
            # Music On
            print(left)
            hub.display.show(hub.Image.YES)
            motors.pwm(left, right)
            utime.sleep(1)
    except:
        print("Except")
        pass

def pdControl(threshold, prev_e, dt):
    # Adjust speed by how far of the line the car is
    try:
        for_error = follower.get()[0] - threshold
        #print('here2')
        curr_e = for_error
        if dt != 0 :
            de = (curr_e - prev_e) / dt
        else :
            de = 0
        #print(for_error)
        turn_rate = (PROPORTIONAL_GAIN * for_error) + (Kd*de)
        #print(turn_rate)
        left_speed = int(base_speed + turn_rate)
        right_speed = int(base_speed - turn_rate)
        #print("Left_s:", left_speed)
        #print("Right_s", right_speed)
        return left_speed, right_speed, curr_e
    except:
        pass

def timeDiff(previous):
    curr = utime.ticks_ms()
    dt = utime.ticks_diff(curr, previous)
    dt = dt / 1000
    
    return dt, curr

def main():
    spinner.pwm(spin_speed)
    threshold = 82 #trainLightSensors()
    prev_t = utime.ticks_ms()
    prev_e = 0
    #print('here1')
    while True :
        #print('hereW')
        dt, curr_t = timeDiff(prev_t)
        
        prev_t = curr_t
        
        left_speed, right_speed, temp_e = pdControl(threshold, prev_e, dt)
        
        prev_e = temp_e
        motors.pwm(-left_speed, right_speed)
        #piMusicDetection(-left_speed, right_speed)
    # Stop Motor
    
    utime.sleep(1)
    motors.pwm(0,0)

main()
spinner.pwm(0)
motors.pwm(0,0)
