import json
import cv2 as cv
import face_recognition
import os

target = input('Enter avatar url: ')
distance = float(input(
    "Enter distance between 2 images (leave blank to set default 0.6): ") or "0.6")
img_folder = input("Enter images folder url(end with '/'): ")
outp_name = input("Enter output file name (include .ext): ")


def read_image(folder):
    fileList = []
    for file in os.listdir(folder):
        fileList.append(folder + file)
    return fileList


def encodeImage(image):
    target = cv.imread(cv.samples.findFile(image))
    img_rgb = cv.cvtColor(target, cv.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(img_rgb)
    return img_encoding


def detectionProcessing(imgFolder, encodedTarget, outputData, distance):
    imageList = read_image(imgFolder)
    for image in imageList:
        encodedImages = encodeImage(image)
        if len(encodedImages) == 0:
            continue
        result = face_recognition.compare_faces(
            encodedImages, encodedTarget, distance)

        if True in result:
            face_distances = face_recognition.face_distance(
                encodedImages, encodedTarget)
            outputData["data"].append(image)
            outputData["distance"].append(min(face_distances))


with open(outp_name, "w") as outputFile:
    encodedTarget = encodeImage(target)[0]
    outputData = {
        "data": [],
        "distance": []
    }
    detectionProcessing(img_folder, encodedTarget, outputData, distance)
    json_object = json.dumps(outputData, indent=4)
    outputFile.write(json_object)
    print(outputData)


cv.waitKey()
