#!/usr/bin/env python3

"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import time
import rospy
from Eyetracking.msg import BoolStateEyetracking



rightGaze_timer = 0
leftGaze_timer = 0 
leftOrRight = 0
gaze = GazeTracking()
webcam = cv2.VideoCapture(2)


def publishing_node_eyetracking():
    rospy.init_node('publishing_node_Eyetracking', anonymous=True)
    rate = rospy.Rate(1)  # 1 Hz

    pub = rospy.Publisher('bool_state_topic_Eyetracking', BoolStateEyetracking, queue_size=10)

    while not rospy.is_shutdown():
        bool_state_msg = BoolStateEyetracking()
        bool_state_data = True
        int_state_data = leftOrRight
        bool_state_msg.bool_data = bool_state_data
        bool_state_msg.int_data = int_state_data
        
        pub.publish(bool_state_msg)

        rate.sleep()



while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # W
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    looking_left = False
    looking_right = False

    if gaze.is_blinking():
        text = "Blinking"
        print("Blink detected!")
        

    elif gaze.is_left():
        text = "Looking left"
        looking_left = True
        looking_right = False
        rightGaze_timer = 0
        if leftGaze_timer == 0:
            leftGaze_timer = time.time()

        elapsed_time = time.time() - leftGaze_timer
        if elapsed_time >= 3.0:
            print("Been in the left case for more than 3 seconds!")
            leftOrRight = 1
            break


    elif gaze.is_center():
        text = "Looking right"
        looking_left = False
        looking_right = True
        leftGaze_timer = 0 
        if rightGaze_timer == 0:
            rightGaze_timer = time.time()

        elapsed_time = time.time() - rightGaze_timer
        if elapsed_time >= 3.0:
            print("Been in the right case for more than 3 seconds!")
            leftOrRight = 2
            break





    print('looking left: ', looking_left)
    print('looking right: ', looking_right)


        

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    
    if cv2.waitKey(1) == 27:
        break

   
webcam.release()
cv2.destroyAllWindows()

 # Write the updated value to the file
try:
    publishing_node_eyetracking()
except rospy.ROSInterruptException:
        pass
