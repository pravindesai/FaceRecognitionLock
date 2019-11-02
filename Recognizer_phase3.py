import cv2
import ctypes
import FaceTrainer_phase2

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id=0
names=FaceTrainer_phase2.names

cam=cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)


while True:
    ret,img=cam.read()
    '''
    # rotation of img
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
    img = cv2.warpAffine(img, M, (cols, rows))
    '''
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray=gray[y:y+h,x:x+w]
        id,confidence=recognizer.predict(roi_gray)
        color = (0, 0, 0)

        # If confidence is less them 100 ==> "0" : perfect match
        if (confidence < 100):
            id = names[id]
            color=(0,255,0)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            ctypes.windll.user32.LockWorkStation()
            color=(0,0,255)
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img,str(id),(x + 5, y - 5),font,1,color,1)
        cv2.putText(img, str(confidence),(x + 5, y + h - 5),font,1,color,1)

    cv2.imshow('camera', img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()