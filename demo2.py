import json
import cv2 as cv
import sys
import face_recognition
import os

print('Enter avatar url:')
target = input()

print("Enter images folder url(end with '/'):")
img_folder = input()

print('Enter output file name (include .ext):')
outp_name = input()


class FileListingInterface:
    def read_image(self):
        pass


class ListFileFromDirectory(FileListingInterface):
    fileList = []

    def __init__(self, folder) -> None:
        self.folder = folder

    def read_image(self):
        for file in os.listdir(self.folder):
            self.fileList.append(self.folder + file)
        return self.fileList


class ListFileFromImagesList(FileListingInterface):
    def __init__(self, imageList) -> None:
        self.imageList = imageList

    def read_image(self):
        return self.imageList


def encodeImage(image):
    target = cv.imread(cv.samples.findFile(image))
    img_encoding = face_recognition.face_encodings(target)
    return img_encoding


def detectionProcessing(fileListingMethod, target_encoding, outputData):
    imageList = fileListingMethod.read_image()
    for file in imageList:

        img_encodings = encodeImage(file)
        if len(img_encodings) == 0:
            continue

        result = face_recognition.compare_faces(
            img_encodings, target_encoding)

        if True in result:
            outputData["data"].append(file)
            outputData["index"].append(result.index(True))


with open(outp_name, "w") as outputFile:
    target_encoding = encodeImage(target)[0]
    tempData = {
        "data": [],
        "index": []
    }
    detectionProcessing(ListFileFromDirectory(
        img_folder), target_encoding, tempData)
    json_object = json.dumps(tempData, indent=4)
    outputFile.write(json_object)

with open(outp_name, "r") as tempImages:
    data = json.load(tempImages)
    images = data["data"]
    indices = data["index"]
    finalData = {
        "data":[]
    }
    # for i in images:
    #     detectionProcessing(ListFileFromImagesList(images),encodeImage(i)[indices[images.index(i)]],finalData)


#  TODO: filter non-related images in "lines"


cv.waitKey()
