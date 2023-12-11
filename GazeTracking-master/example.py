import cv2
from gaze_tracking import GazeTracking
import time

# Create GazeTracking object and open webcam
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Initialize timer variables
tSample = 0.1
start_time = time.time()
tTimetoSample = time.time()
blink_count = 0
print(start_time)

# Set cooldown duration for blink detection (in seconds)
cooldown_duration = 0.15
last_blink_time = 0

# Main loop
while True:
    tGlobal = time.time()

    if tTimetoSample <= tGlobal:
        tStartloop = time.time()
        tTimetoSample = tTimetoSample + tSample

        # Read frame from the webcam
        _, frame = webcam.read()

        # Refresh gaze data for the current frame
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        text = ""

        looking_left = False
        looking_right = False

        # Check gaze direction and update variables 
        if gaze.is_blinking():
            current_time = time.time()
            # Check if cooldown period has passed since the last blink
            if current_time - last_blink_time >= cooldown_duration:
                text = "Blinking"
                blink_count += 1
                last_blink_time = current_time  # Update last blink time
                print("Blink detected! Total blinks:", blink_count)

                # Check for three blinks within a two-second window
                if blink_count >= 3 and current_time - start_time <= 2:
                    print("Pop-up window!")

                    # Reset the counter and start time
                    blink_count = 0
                    start_time = time.time()
        

        elif gaze.is_left():
            text = "Looking left"
            looking_left = True
            looking_right = False
        elif gaze.is_center():
            text = "Looking right"
            looking_left = False
            looking_right = True

        # Display gaze information on the frame
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        
        # Display the annotated frame
        cv2.imshow("Demo", frame)

        # Check for the 'Esc' key to exit the loop
        if cv2.waitKey(1) == 27:
            break

# Release webcam and close OpenCV windows
webcam.release() 
cv2.destroyAllWindows()
