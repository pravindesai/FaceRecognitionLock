import cv2
import FaceTrainer_phase2
import diloag
diloag.main().exe()
uid=diloag.uid
#print(uid)

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('./LBP.xml') #Local Binary Pattern
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
i=0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10, 10))
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(img, str(i), (x, h), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        cv2.imwrite("./user/User." + str(uid) + '.' +
                    str(i) + ".jpg", roi_gray)
        i=i+1
    cv2.imshow('video',img)
    if cv2.waitKey(1) == ord('q') or i>=100:
        break

cap.release()
cv2.destroyAllWindows()
FaceTrainer_phase2.Train().TrainModel()
