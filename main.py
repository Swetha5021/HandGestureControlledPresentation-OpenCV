# HAND GESTURE CONTROLLED PRESENTATION USING OPENCV
# Made by Sruthi Sivasankararaj
# CSE, RMKEC

import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

width, height = 1280, 720
folderPath = "Presentation"

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pathImages = sorted(os.listdir(folderPath), key=len)

#Variables

imgNumber = 0
hs, ws = int(120 * 2.5), int(213 * 2.5)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 27
annotations = [[]]
annotationNumber = -1
annotationStart = False
pointerX, pointerY = 0, 0

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    #cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']

        indexFinger = lmList[8][0], lmList[8][1]
        xVal = int(np.interp(lmList[8][0], [width//2, width], [0, ws]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, hs]))
        #indexFinger = xVal, yVal

        #Gesture 1 - Previous Slide
        if fingers == [1,0,0,0,0]:
                print('Left')

                annotations = [[]]
                annotationNumber = -1
                annotationStart = False

                if imgNumber>0:
                    buttonPressed = True
                    imgNumber -= 1
        
        #Gesture 2 - Next Slide    
        if fingers == [0,0,0,0,1]:
            print('Right')

            annotations = [[]]
            annotationNumber = -1
            annotationStart = False

            if imgNumber < len(pathImages) - 1:
                buttonPressed = True
                imgNumber += 1

        #Gesture 3 - Holding the Pointer            
        if fingers == [0,1,1,0,0]:
            print('Holding')
            x, y = lmList[8][0], lmList[8][1]
            pointerX = int(np.interp(x, [0, width], [0, imgCurrent.shape[1]]))
            pointerY = int(np.interp(y, [0, height], [0, imgCurrent.shape[0]]))
            cv2.circle(imgCurrent, (pointerX, pointerY), 12, (0, 0, 255), cv2.FILLED)

        #Gesture 4 - Drawing on the Slide
        if fingers == [0,1,0,0,0]:
            print('Drawing')
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            
            x, y = lmList[8][0], lmList[8][1]
            pointerX = int(np.interp(x, [0, width], [0, imgCurrent.shape[1]]))
            pointerY = int(np.interp(y, [0, height], [0, imgCurrent.shape[0]]))
            cv2.circle(imgCurrent, (pointerX, pointerY), 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append((pointerX, pointerY))
        else:
            annotationStart = False

        #Gesture 5 - Erasing
        if fingers == [0,1,1,1,0]:
            print('Erasing')
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
    else:
        annotationStart = False
    
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter>buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j],(0, 0, 255), 12)

    imgSmall = cv2.resize(img, (ws, hs))

    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall

    imgCurrent = cv2.resize(imgCurrent, (int(width * 0.7), int(height * 0.7)))

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    #Quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

