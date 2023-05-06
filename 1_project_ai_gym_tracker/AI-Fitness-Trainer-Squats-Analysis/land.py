import mediapipe as mp
import cv2

# Initialize the MediaPipe Pose model
mp_pose = mp.solutions.pose.Pose()

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Use the MediaPipe Pose model to detect landmarks in the frame
    results = mp_pose.process(frame_rgb)

    # Extract the landmarks from the results
    landmarks = results.pose_landmarks

    # Do something with the landmark positions

    # Display the frame
    cv2.imshow('Frame', frame)

    # Check if the user has pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()

print(landmarks)
