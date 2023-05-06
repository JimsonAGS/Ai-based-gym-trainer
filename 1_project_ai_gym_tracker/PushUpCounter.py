import cv2
import numpy as np
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"

while cap.isOpened():
    ret, img = cap.read()  # 640 x 480
    # Determine dimensions of video - Help with creation of box in Line 43
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:


        # Check to ensure right form before starting the program
        angle = detector.findAngle(img, 11, 13, 15)

        angle_knee = detector.findAngle(img, 23, 25, 27)

        angle_hip = detector.findAngle(img, 11, 23, 25)

        per = np.interp(angle_knee, (90, 160), (0, 100))

        # Bar to show Pushup progress
        bar = np.interp(angle_knee, (90, 160), (380, 50))

        # Check for full range of motion for the pushup
        if angle_knee > 169:
            stage = "UP"
        if angle_knee <= 90 and stage == 'UP':
            stage = "DOWN"
            count += 1

        print(count)

        # Draw Bar

        cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 2)

        # Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        # Feedback
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    cv2.imshow('Squat', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()