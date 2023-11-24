import dlib

detector = dlib.get_frontal_face_detector()

def validateFace(imagePath):
    print("Processing file: {}".format(imagePath))
    img = dlib.load_rgb_image(imagePath)
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    dets = detector(img, 1)
    count = len(dets)
    return count == 1
   