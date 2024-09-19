import cv2


rstp = [
    "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
    "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
    "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
    "http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg",
]
cap = cv2.VideoCapture(rstp)

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
