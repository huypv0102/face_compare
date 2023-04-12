import json
import cv2 as cv
import face_recognition
import os

target = input('Enter avatar url: ')
distance = float(input(
    "Enter distance between 2 images (leave blank to set default 0.6): ") or "0.6")
imgFolder = input("Enter images folder url(end with '/'): ")
outputFileName = input("Enter output file name (include .ext): ")


def readFiles(folder):
    fileList = []
    for file in os.listdir(folder):
        fileList.append(folder + file)
    return fileList


def encodeFaces(image):
    target = cv.imread(cv.samples.findFile(image))
    img_rgb = cv.cvtColor(target, cv.COLOR_BGR2RGB)
    encodedFaces = face_recognition.face_encodings(img_rgb)
    return encodedFaces


def detectionProcessing(imgFolder, encodedTarget, outputData, distance):
    imageList = readFiles(imgFolder)
    for image in imageList:
        encodedFaces = encodeFaces(image)
        if len(encodedFaces) == 0:
            continue
        comparedFaces = face_recognition.compare_faces(
            encodedFaces, encodedTarget, distance)

        if True in comparedFaces:
            faceDistances = face_recognition.face_distance(
                encodedFaces, encodedTarget)
            outputData["data"].append(image)
            outputData["distance"].append(min(faceDistances))


with open(outputFileName, "w") as outputFile:
    encodedTarget = encodeFaces(target)[0]
    outputData = {
        "data": [],
        "distance": []
    }
    detectionProcessing(imgFolder, encodedTarget, outputData, distance)
    json_object = json.dumps(outputData, indent=4)
    outputFile.write(json_object)
    print(outputData)


cv.waitKey()
