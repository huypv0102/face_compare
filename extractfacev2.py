import cv2
import dlib
from time import time
import matplotlib.pyplot as plt

hog_face_detector = dlib.get_frontal_face_detector()


def hogDetectFaces(imagePath,extractedFolder,  display = False):
    image = cv2.imread(imagePath)

    height, width, _ = image.shape

    output_image = image.copy()

    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    start = time()

    results = hog_face_detector(imgRGB, 0)
    end = time()

    for bbox in results:

        x1 = bbox.left()
        y1 = bbox.top()
        x2 = bbox.right()
        y2 = bbox.bottom()

        # cv2.rectangle(output_image, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=width//200)  
        roi_color = image[y1:y2, x1:x2]
        cv2.imwrite(extractedFolder + "/"+ str(x2) + str(y2)+".jpg", roi_color)
    if display:

        cv2.putText(output_image, text='Time taken: '+str(round(end - start, 2))+' Seconds.', org=(10, 65),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=width//700, color=(0,0,255), thickness=width//500)

        plt.figure(figsize=[15,15])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output");plt.axis('off');
        plt.show()

    else:

        return output_image, results

