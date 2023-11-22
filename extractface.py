import cv2
import os

def extractFace(imagePath):
    img = cv2.imread(imagePath)

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        "haarcascade_frontalface_default (1).xml"
    )
    
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10)
    )
    return [face,img]


def extractFaceToMemory(imagePath):
    [face,img] = extractFace(imagePath)    
    faces =[]
    for (x, y, w, h) in face:
        roi_color = img[y:y + h, x:x + w]
        faces.append(roi_color)
    return faces


def extractFaceToFolder(imagePath,extractedFolder):
    
    [face,img] = extractFace(imagePath)    
    for (x, y, w, h) in face:
        roi_color = img[y:y + h, x:x + w]
        folderName = extractedFolder  ;
        cv2.imwrite(folderName + "/"+ str(w) + str(h)+".jpg", roi_color)

