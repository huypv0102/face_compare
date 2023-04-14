import json
import cv2 as cv
import face_recognition
import os
import sys
import tqdm

target = input('Avatar url: ')
distance = float(input(
    "Base distance used for 'final distance' looking up (leave blank to set default 0.3): ") or "0.3")
increase =  float(input(
    "Step size for each duration (leave blank to set default 0.01): ") or "0.01")
imgFolder = input("Image folder url (end with '/'): ")
outputFileName = input("Output file name: ")


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


def findImages(imageList, encodedTarget, distance, outputData):

    bar = tqdm.tqdm(total=len(imageList), desc="Find images with distance " + str(distance), position=1)
    for image in imageList:
        bar.update(1)
        tmpDist = findDistance(image, encodedTarget)
        if (tmpDist != -1 and tmpDist <= distance):
            outputData["data"].append(image)
            outputData["distance"].append(tmpDist)


def findFinalDistance(imageList, encodedTarget, baseDistance, increase):
    distance = baseDistance
    while distance <= 0.6:
        bar = tqdm.tqdm(total=len(imageList), desc="Find correct distance from " + str(distance), position=1)
        for image in imageList:
            tmpDist = findDistance(image, encodedTarget)
            bar.update(1)
            if (tmpDist == -1):
                continue
            if tmpDist >= baseDistance and tmpDist <= distance:
                return tmpDist
        distance = distance + increase
    return -1


def findDistance(image, encodedTarget):
    encodedFaces = encodeFaces(image)
    if len(encodedFaces) == 0:
        return -1
    return min(face_recognition.face_distance(
        encodedFaces, encodedTarget))


with open(outputFileName, "w") as outputFile:
    encodedTarget = encodeFaces(target)[0]
    outputData = {
        "data": [],
        "distance": []
    }
    imageList = readFiles(imgFolder)
    distance = findFinalDistance(imageList, encodedTarget, distance, increase)
    if (distance == -1):
        sys.exit("Re-adjust the distance for more correct result")
    findImages(imageList, encodedTarget, distance, outputData)
    json_object = json.dumps(outputData, indent=4)
    outputFile.write(json_object)
    print(outputData)


cv.waitKey()
