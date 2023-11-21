import cv2 as cv


faceCascade = cv.CascadeClassifier("haarcascade_frontalface_default (1).xml")
eyeCascade = cv.CascadeClassifier("haarcascade_eye.xml")
# nose_classifier = cv.CascadeClassifier("haarcascade_mcs_nose.xml")
# mouth_classifier = cv.CascadeClassifier("haarcascade_mcs_mouth.xml")

def validateFace(imagePath):
    image = cv.imread(imagePath)
    if (image is None):
        return False
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
    )
 

    eyes = []
    mouth=[]
    nose = []
    for (x, y, w, h) in faces:
        # cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eyeCascade.detectMultiScale(roi_gray)
        # mouth = mouth_classifier.detectMultiScale(roi_gray)
        # nose = nose_classifier.detectMultiScale(roi_gray)

    result = {
        "faces": len(faces),
        "eyes": len(eyes),
        # "mouth":len(mouth),
        # "nose":len(nose),
        
    }
    return result["faces"] == 1 and result["eyes"] == 2 



