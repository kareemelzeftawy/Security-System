import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# initialize the motors
GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

#Motor1 Initialization
Motor1A = 27
Motor1B = 22
Motor1E = 17
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

#Motor2 Initialization
Motor2A = 24
Motor2B = 23
Motor2E = 25
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

#Motor3 Initialization
Motor3A = 9
Motor3B = 11
Motor3E = 10
GPIO.setup(Motor3A,GPIO.OUT)
GPIO.setup(Motor3B,GPIO.OUT)
GPIO.setup(Motor3E,GPIO.OUT)

#Motor4 Initialization
Motor4A = 8
Motor4B = 7
Motor4E = 12
GPIO.setup(Motor4A,GPIO.OUT)
GPIO.setup(Motor4B,GPIO.OUT)
GPIO.setup(Motor4E,GPIO.OUT)

#Push_Button Initialization
Button = 20
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#button = Button(16)

def Motor1_Forward():
    print ("Motor1 Going forwards")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    
def Motor2_Forward():
    print ("Motor2 Going forwards")
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def Motor3_Forward():
    print ("Motor3 Going forwards")
    GPIO.output(Motor3A,GPIO.HIGH)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor3E,GPIO.HIGH)

def Motor4_Forward():
    print ("Motor4 Going forwards")
    GPIO.output(Motor4A,GPIO.HIGH)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.output(Motor4E,GPIO.HIGH)

def Motor1_Backward():
    print ("Motor1 Going backwards")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

def Motor2_Backward():
    print ("Motor2 Going backwards")
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def Motor3_Backward():
    print ("Motor3 Going backwards")
    GPIO.output(Motor3A,GPIO.LOW)
    GPIO.output(Motor3B,GPIO.HIGH)
    GPIO.output(Motor3E,GPIO.HIGH)

def Motor4_Backward():
    print ("Motor4 Going backwards")
    GPIO.output(Motor4A,GPIO.LOW)
    GPIO.output(Motor4B,GPIO.HIGH)
    GPIO.output(Motor4E,GPIO.HIGH)

def Motor1_Stop():
    print ("Motor1 Stop")
    GPIO.output(Motor1E,GPIO.LOW)

def Motor2_Stop():
    print ("Motor2 Stop")
    GPIO.output(Motor2E,GPIO.LOW)

def Motor3_Stop():
    print ("Motor3 Stop")
    GPIO.output(Motor3E,GPIO.LOW)

def Motor4_Stop():
    print ("Motor4 Stop")
    GPIO.output(Motor4E,GPIO.LOW)

def Motor_Sequence():
    #Motor1 forward for 5 Seconds
    Motor1_Forward()
    time.sleep(5)
    Motor1_Stop()

    #Motor2 forward for 5 Seconds
    Motor2_Forward()
    time.sleep(5)
    Motor2_Stop()

    #Motor3 forward for 5 Seconds
    Motor3_Forward()
    time.sleep(5)
    Motor3_Stop()

    #Motor4 forward for 5 Second
    Motor4_Forward()
    time.sleep(5)
    Motor4_Stop()

    #wait untill the button pressed
    print("Wait till the button pressed")
    #button.wait_for_press()
    GPIO.wait_for_edge(Button, GPIO.FALLING)
    print("The button pressed")
    
    #Motor1 Backward for 5 Seconds
    Motor1_Backward()
    time.sleep(5)
    Motor1_Stop()

    #Motor2 Backward for 5 Seconds
    Motor2_Backward()
    time.sleep(5)
    Motor2_Stop()

    #Motor3 backward for 5 Seconds
    Motor3_Backward()
    time.sleep(5)
    Motor3_Stop()

    #Motor4 backward for 5 Seconds
    Motor4_Backward()
    time.sleep(5)
    Motor4_Stop()

#Main
Motor_Sequence()
