# import the necessary packages
from imutils.video import VideoStream
import time
import cv2
import face_recognition
from multiprocessing import Process
from multiprocessing import Queue
import datetime
import sys
from Naked.toolshed.shell import muterun_js
import RPi.GPIO as GPIO

# initialize the video stream and allow the camera
# sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

#disable warnings
GPIO.setwarnings(False)

# initialize the motors
GPIO.setmode(GPIO.BCM)

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

# initialize the input queue (frames), output queue (detections),
# and the list of actual detections returned by the child process
FrameQueue = Queue(maxsize=1)
Recording_flag = Queue(maxsize=1)
Recording_path = Queue(maxsize=1)
Motor_flag = Queue(maxsize=1)
#NFC_flag = Queue(maxsize=2)
#Stream_flag = Queue(maxsize=1)
detection_flag = Queue(maxsize=1)

def Recording(FrameQueue, Recording_flag, Recording_path, Motor_flag):
    # initialize the FourCC, video writer, dimensions of the frame
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    flag = False
    while True:
        if not Recording_flag.empty():
            # grab the frame from the input queue, resize it
            flag = Recording_flag.get()
            if flag == True:
                print("Start Recording")
                #grab the video path
                Video_Path = Recording_path.get()
                # store the image dimensions, initialzie the video writer,
                writer = cv2.VideoWriter(Video_Path, fourcc, 20.0, (640,480))
                #the Recording time
                end = datetime.datetime.now() + datetime.timedelta(seconds=5)
                # keep looping
                while (end > datetime.datetime.now()):
                    # check to see if there is a frame in our input queue
                    if not FrameQueue.empty():
                        # grab the frame from the input queue, resize it
                        frame = FrameQueue.get()
                        # write the output frame to file
                        writer.write(frame)
                print("Finish Recording")
                #Release the writer
                writer.release()
                flag = False
                Motor_flag.put(True)
                    
def Face_Detection(detection_flag, FrameQueue, Recording_flag):
    # Initialize Detection variables
    face_locations = []
    process_this_frame = True
    flag = False
    while True:
        # check to see if there is a frame in our input queue
        if not detection_flag.empty():
            # grab the frame from the input queue, resize it
            flag = detection_flag.get()
        # keep looping
        while flag is True:
            # check to see if there is a frame in our input queue
            if not FrameQueue.empty():
                # grab the frame from the input queue, resize it
                frame = FrameQueue.get()
                #detect the face every two frames
                if process_this_frame:
                    # Resize frame of video to 1/4 size for faster face recognition processing
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(small_frame, number_of_times_to_upsample=1, model="cnn")
                    #Check if detect faces
                    if len(face_locations) > 0:
                        print("I found {} face(s) in this Frame.".format(len(face_locations)))
                        #Enable the Recording
                        Recording_flag.put(True)
                        #disable the Detection flag
                        #detection_flag.put(False)
                        #break the flag while
                        flag = False
                        print("Detect Face!")
                process_this_frame = not process_this_frame

def Grab_Frame_and_Stream():
    # grab the frame from the video stream
    frame = vs.read()
    
    # if the inqput queue *is* empty, give the current frame to
    # classify
    if FrameQueue.empty():
        FrameQueue.put(frame)
      
    # show the frames
    cv2.imshow("Frame", frame)

def Read_NFC_Card():
    response = muterun_js('/home/pi/Desktop/mifare-classic-js/examples/read.js')
    message = response.stdout
    message = message.decode('ascii').replace('Text Record\n','')
    message = message.replace('\n\n',',').split(',')
    return message

def Check_NFC_Card(message):
    if message[0] is not '\n':
        return True
    else:
        return False

def Check_NDEF_Message(message):
    #Check the Card
    if (message[0] == '86fd3b07') and (message[1] == 'Mohammed') and (message[2] == 'Robotics') and (message[3] == '123456789'):
        print("Valid Card!")
        return True
    else:
        print("Invalid Card!")
        return False

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
    
    #Motor1 forward for 10 Seconds
    Motor1_Forward()
    time.sleep(10)
    Motor1_Stop()

    #Motor2 forward
    Motor2_Forward()

    #Motor3 forward for 2 Seconds
    Motor3_Forward()
    time.sleep(2)
    Motor3_Stop()

    #Motor4 forward for 1 Second
    Motor4_Forward()
    time.sleep(1)
    Motor4_Stop()

    #wait untill the button pressed
    print("Wait till the button pressed")
    #button.wait_for_press()
    GPIO.wait_for_edge(Button, GPIO.FALLING)
    print("The button pressed")
    
    #Motor2 Stop
    Motor2_Stop()

    #Motor3 backward for 1 Second
    Motor3_Backward()
    time.sleep(1)
    Motor3_Stop()

    #Wait for 3 Seconds
    time.sleep(3)

    #Motor1 backward for 10 Seconds
    Motor1_Backward()
    time.sleep(10)
    Motor1_Stop()

#Intialize some variables for the flags
#For the Stream_Flag
Stream = False

# construct a child process *indepedent* from our main process of
# execution
print("[INFO] starting Recording Process...")
p = Process(target=Recording, args=(FrameQueue, Recording_flag, Recording_path, Motor_flag))
p.daemon = True
p.start()        

print("[INFO] starting Detection Process...")
s = Process(target=Face_Detection, args=(detection_flag, FrameQueue, Recording_flag))
s.daemon = True
s.start()

#Waiting for an NFC Card
print('Waiting for an NFC Card!')

#Main Loop
while True:
    
    #Read the NFC Card
    message = Read_NFC_Card()
    #Check if there's a NFC Card or not!
    Status = Check_NFC_Card(message)
    # if there's a NFC Card
    if Status == True:
        #check if the Card valid or not
        validation = Check_NDEF_Message(message)
        #if the card valid
        if validation == True:
            #Start the Streaming
            Stream = True
            #the Recording video path
            Recording_path.put('/home/pi/Desktop/Security_System/Videos/valid.avi')
            #detection process will start
            detection_flag.put(True)
            #empty the message variable
            message = []
            print("Waiting till detect a Face")
            #Turn on the Motors sequence
            while is not Motor_flag.empty()
            Stream = False
            Motor_Sequence()
            #resume reading NFC Cards
            print('Waiting for an NFC Card!')
                
        #if the card not valid    
        else:
            #the Recording video path
            Recording_path.put('/home/pi/Desktop/Security_System/Videos/Invalid.avi')
            #Recording process will start
            Recording_flag.put(True)
            #empty the message variable
            message = []
                
    # if the stream flag *is not* empty, grab it
    #if not Stream_flag.empty():
        #Stream = Stream_flag.get()
        
    #Check if it will read and stream the frame or not?                
    if Stream == True:
        #read the frame and stream it
        Grab_Frame_and_Stream()

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

#clean up the GPIO
GPIO.cleanup()

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
