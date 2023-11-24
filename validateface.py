import cv2 as cv


faceCascade = cv.CascadeClassifier("haarcascades\haarcascade_frontalface_alt.xml")
eyeCascade = cv.CascadeClassifier("haarcascades\haarcascade_eye.xml")

def extractFacePart(image,faces):
    eyes = []
    for (x, y, w, h) in faces:
    
        roi_image = image[y:y+h, x:x+w]
        # cv.rectangle(roi_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv.imshow('img',roi_image)
        # cv.waitKey(0)
        eyes.append( eyeCascade.detectMultiScale(roi_image))

    return [eyes,faces]

    


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
    [eyes,faces] = extractFacePart(image,faces)
    # print(len(eyes), len(faces)) 


    result = {
        "faces": len(faces),
        "eyes": len(eyes),
        
    }
    return result["faces"] == 1 and result["eyes"] >= 1 



