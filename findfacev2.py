import os,shutil
import face_recognition
import argparse
import extractface
import json
import cv2 
import validateface
import validatefacev2
import extractfacev2
from pathlib import Path

EXTRACTEDFOLDER = "extractedFolder/"
if not os.path.exists(EXTRACTEDFOLDER):
    os.makedirs(EXTRACTEDFOLDER) 

RESULTFILE = "result.txt"
OUTPUTDATA = {
    "data":[]
}

def listAllImage(imageFolder):
    imageFiles = []
    for path, subdirs, files in os.walk(imageFolder):
        for name in files:
            imageFiles.append(os.path.join(path, name))
    return imageFiles


def writeToFile(fileName):
    with open(fileName, "w") as outputFile:
        json_object = json.dumps(OUTPUTDATA, indent=4)
        outputFile.write(json_object)


# 1 train image && 1 face
def train(imagePath):
    model="hog"
    encoded = []
    image = face_recognition.load_image_file(imagePath)
    faceLocations = face_recognition.face_locations(image, model=model)
    faceEncodings = face_recognition.face_encodings(image, faceLocations)
    encoded.append(faceEncodings[0])
    return encoded

def findFace(targetPath,imageFolder):
    if not validatefacev2.validateFace(targetPath):
        print("No valid face")
        return
    OUTPUTDATA["data"].append(targetPath)
    
    encodedTarget = train(targetPath)
    
    for image in listAllImage(imageFolder):
        # extract face
        # extractface.extractFaceToFolder( image,extractedFolder)
        extractfacev2.hogDetectFaces(image,EXTRACTEDFOLDER)

        for extracted in os.listdir(EXTRACTEDFOLDER):

            facePath = EXTRACTEDFOLDER  + extracted
            face = face_recognition.load_image_file(facePath)
            faceEncoding = face_recognition.face_encodings(face)
            
            if len(faceEncoding) !=0:
                results = face_recognition.compare_faces(encodedTarget, faceEncoding[0],0.28)
                if False not in results:
                    print( image )

        
            # remove face files
            os.remove(facePath)
        
    writeToFile(RESULTFILE)
    
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Target", help="Target path", required=True)
    parser.add_argument("-f", "--Folder", help="Image folder(end with '/')", required=True)
    args = parser.parse_args()

    findFace(args.Target, args.Folder)
    