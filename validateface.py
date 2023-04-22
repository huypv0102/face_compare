import cv2 as cv
import argparse

faceCascade = cv.CascadeClassifier("haarfrontface.xml")
eyeCascade = cv.CascadeClassifier("haareye.xml")
fullBodyCascade = cv.CascadeClassifier("haarfullbody.xml")
upperBodyCascade = cv.CascadeClassifier("haarupperbody.xml")


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
    fullBody = fullBodyCascade.detectMultiScale(
        gray,
    )
    upperBody = upperBodyCascade.detectMultiScale(
        gray,
    )

    eyes = []
    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eyeCascade.detectMultiScale(roi_gray)

    result = {
        "faces": len(faces),
        "eyes": len(eyes),
        "fullBody": len(fullBody),
        "upperBody": len(upperBody),
    }
    print(result)
    return result["faces"] == 1 and result["eyes"] == 2 and result["upperBody"] <= 1 and result["fullBody"] <= 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Target", help="Target path", required=True)
    args = parser.parse_args()

    print(validateFace(imagePath=args.Target))

cv.waitKey()
