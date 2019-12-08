from datetime import datetime

import cv2
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Students']
user = db.user

col_name = 'day' + str(datetime.now().strftime('%d_%m_%Y'))
attendance = db[col_name]


def setAB(number_of_students):
    # print(number_of_students)
    for n in range(1, number_of_students + 1):
        d = {
            'id': str(n),
            'val': 'A'
        }
        attendance.insert_one(d)


if attendance.count_documents({}) == 0:
    # print(user.count_documents({}))
    setAB(user.count_documents({}))


def markPresent(id, name):
    updateDict = {
        'id': str(id),
        'val': 'P'
    }
    print(attendance.update_one({'id': str(id)}, {'$set': updateDict}))
    print(id, ': PRESENT')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "./haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        id, confidence = recognizer.predict(roi_gray)
        color = (0, 0, 0)

        # If confidence is less them 100 ==> "0" : perfect match
        if (confidence < 100):
            name = str(user.find_one({'id': str(id)}, {'name': 1})['name'])
            markPresent(id, name)
            color = (0, 255, 0)
            confidence = str(round(100 - confidence)) + '%'
        else:
            name = "unknown"
            color = (0, 0, 255)
            confidence = str(round(100 - confidence)) + '%'

        cv2.putText(img, str(id) + ' : ' + str(name), (x + 5, y - 5), font, 1, color, 1)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, color, 1)

    cv2.imshow('camera', img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
