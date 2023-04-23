import json
import cv2 as cv
import face_recognition
import os
import sys
import tqdm
import argparse
import validateface
import createvideo


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

    bar = tqdm.tqdm(total=len(
        imageList), desc="Find images with distance " + str(distance), position=1)
    for image in imageList:
        bar.update(1)
        tmpDist = findDistance(image, encodedTarget)
        if (tmpDist != -1 and tmpDist <= distance):
            outputData["data"].append(image)


def findFinalDistance(imageList, encodedTarget, baseDistance, increase):
    distance = baseDistance
    while distance <= 0.5:
        bar = tqdm.tqdm(total=len(
            imageList), desc="Find correct distance from " + str(distance), position=1)
        for image in imageList:
            tmpDist = findDistance(image, encodedTarget)
            bar.update(1)
            if (tmpDist == -1):
                continue
            if (tmpDist > 0.5):
                imageList.remove(image)
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


def findfaces(outputFileName, target, imgFolder, distance, increase):
    isValid = validateface.validateFace(target)
    if (isValid != True):
        return False
    with open(outputFileName, "w") as outputFile:
        encodedTarget = encodeFaces(target)[0]
        outputData = {
            "data": [],
        }
        outputData["data"].append(target)
        imageList = readFiles(imgFolder)
        distance = findFinalDistance(
            imageList, encodedTarget, distance, increase)
        if (distance == -1):
            sys.exit("Re-adjust the distance for more correct result")
        findImages(imageList, encodedTarget, distance, outputData)
        json_object = json.dumps(outputData, indent=4)
        outputFile.write(json_object)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Target", help="Target path", required=True)
    parser.add_argument("-d", "--Distance",
                        help="Base distance ", default=0.3, type=float)
    parser.add_argument("-i", "--Increase",
                        help="Step size ", default=0.01, type=float)
    parser.add_argument(
        "-f", "--Folder", help="Image folder(end with '/')", required=True)
    parser.add_argument(
        "-o", "--Output", help="Output name", default="result.txt")
    parser.add_argument(
        "-n", "--Name", help="Student name", default="")
    args = parser.parse_args()

    findfaces(distance=args.Distance, outputFileName=args.Output,
              target=args.Target, imgFolder=args.Folder, increase=args.Increase)
