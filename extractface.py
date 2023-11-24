import cv2
import os

def extractFace(imagePath):
    img = cv2.imread(imagePath)

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        "haarcascades\haarcascade_frontalface_alt.xml"
    )
    
    faces = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
  
  
    return [faces,img]


def extractFaceToMemory(imagePath):
    [face,img] = extractFace(imagePath)    
    faces =[]
    for (x, y, w, h) in face:
        roi_color = img[y:y + h, x:x + w]
        faces.append(roi_color)
    return faces


def extractFaceToFolder(imagePath,extractedFolder):
    
    eyeCascade = cv2.CascadeClassifier("haarcascades\haarcascade_eye.xml")
    [face,img] = extractFace(imagePath)    
    for (x, y, w, h) in face:
        roi_color = img[y:y + h, x:x + w]
        eyes = eyeCascade.detectMultiScale(roi_color, scaleFactor=1.1, minNeighbors=5)
        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        
        if len(eyes) >=2:
            cv2.imwrite(extractedFolder + "/"+ str(w) + str(h)+".jpg", roi_color)

