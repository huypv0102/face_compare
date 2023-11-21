import cv2
import os


def extractFaceToFolder(imageFolder,extractedFolder):
    
    images = os.listdir(imageFolder)
    for image in images:

        img = cv2.imread(imageFolder+image)

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(
            "haarcascade_frontalface_default (1).xml"
        )
       
        face = face_classifier.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10)
        )

        
        for (x, y, w, h) in face:
            roi_color = img[y:y + h, x:x + w]
           
            folderName = extractedFolder + image ;
           
            if not os.path.exists(folderName):
                os.makedirs(folderName) 
            # print("[INFO] Object found. Saving to ",folderName)
            cv2.imwrite(folderName + "/"+ str(w) + str(h)+".jpg", roi_color)

