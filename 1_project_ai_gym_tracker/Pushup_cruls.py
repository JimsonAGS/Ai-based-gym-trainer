import time
import PoseModule1 as pm1
import cv2
import numpy as np
import PoseModule as pm
import pyttsx3
import threading

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-35)


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


i='q'
j=0

cap = cv2.VideoCapture(0)
while cap.isOpened():

    ret, img = cap.read()

    width = cap.get(3)
    height = cap.get(4)
    box_size = 150
    center_x = int(width / 2)
    center_y = int(height / 2)
    box1_x = center_x - int(box_size * 1.5)
    box1_y = center_y - int(box_size / 2)

    # Draw the first box on the image

    blur = cv2.GaussianBlur(img, (15,15), 0)
    cv2.rectangle(blur, (center_x - 100, center_y - 100), (center_x + box_size, center_y + box_size), (255, 255, 0), -1)
    cv2.putText(blur, 'BICEP CRUL', (center_x - 50, center_y), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 2)
    # Calculate the coordinates for the second box

    # Draw the second box on the image
    cv2.putText(blur, 'PUSHUP', (center_x - 50, center_y + 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 2)
    cv2.putText(blur, 'SQUAT', (center_x - 50, center_y + 100), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 2)
    cv2.imshow('choose one option', blur)
    if cv2.waitKey(10) & 0xFF == ord('c'):
        i='c'
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(10) & 0xFF == ord('p'):
        i='p'
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(10) & 0xFF == ord('s'):
        i='s'
        cv2.destroyAllWindows()
        break
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
    cv2.waitKey(1)
    """if (j==0):
        t1 = threading.Thread(target=speak("Welcome! Please choose one of the following exercise modes to begin your workout"
                                           " : For Bicep crul press C "
                                           ",For pushup press P "
                                           ", For squat press S,"
                                           "  to close please press Q"))
        t1.start()
        j += 1"""
if(i=='c'):

    def crul():
        detector = pm1.poseDetector()
        count = 0
        dir = 0
        pTime = 0
        while True:
            success, img = cap.read()
            width = cap.get(3)  # float `width`
            height = cap.get(4)
            # img = cv2.imread("AiTrainer/test.jpg")
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            if len(lmList) != 0:
                # Right Arm
                angle = detector.findAngle(img, 12, 14, 16)
                # # Left Arm
                # angle = detector.findAngle(img, 11, 13, 15,False)
                per = np.interp(angle, (210, 310), (0, 100))
                bar = np.interp(angle, (220, 310), (380, 50))
                # print(angle, per)

                # Check for the dumbbell curls
                color = (255, 0, 255)
                if per == 100:
                    color = (0, 255, 0)
                    if dir == 0:
                        count += 0.5
                        dir = 1
                if per == 0:
                    color = (0, 255, 0)
                    if dir == 1:
                        count += 0.5
                        dir = 0


                print(count)

                # Draw Bar

                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

                # Draw Curl Count
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                            (255, 0, 0), 5)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime


            cv2.putText(img, "When performing a bicep curl, keep your elbows stationary and focus "
                             , (0, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)
            cv2.putText(img,"on using your bicep muscles to lift the weight.", (0, 40), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 0, 0), 1)


            cv2.imshow("Image", img)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


    t2 = threading.Thread(target=crul())



elif(i=='p'):
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
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23, 25)

            # Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            # Check to ensure right form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1

            # Check for full range of motion for the pushup
            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"

                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"
                        # form = 0

            print(count)

            # Draw Bar
            if form == 1:
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

        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
elif(i=='s'):
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