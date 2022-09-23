import cv2

vcap = cv2.VideoCapture("rtsp://admin:-arngnennscfrer2@192.168.2.64/Streaming/Channels/101/")

while(1):
    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)