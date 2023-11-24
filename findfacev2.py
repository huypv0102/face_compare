import os,shutil
import face_recognition
import argparse
import extractface
import json
import cv2 
import validateface
import validatefacev2
import extractfacev2


outputData = {
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
        json_object = json.dumps(outputData, indent=4)
        outputFile.write(json_object)


def findFace(targetPath,imageFolder):
    if not validatefacev2.validateFace(targetPath):
        print("No valid face")
        return
    outputData["data"].append(targetPath)
    target = face_recognition.load_image_file(targetPath)
    encodedTarget = face_recognition.face_encodings(target)[0]
    
    extractedFolder = "extractedFolder/"
    if not os.path.exists(extractedFolder):
        os.makedirs(extractedFolder) 
    
    # images = os.listdir(imageFiles)
    imageFiles = listAllImage(imageFolder)
    resultFile = "result.txt"
    for image in imageFiles:
        # extractface.extractFaceToFolder( image,extractedFolder)
        extractfacev2.hogDetectFaces(image,extractedFolder)
        
        extractedImages = os.listdir(extractedFolder )

        for extracted in extractedImages:
            facePath = extractedFolder  + extracted
            face = face_recognition.load_image_file(facePath)
            faceEncoding = face_recognition.face_encodings(face)
            
            if len(faceEncoding) != 0:
                distance = face_recognition.face_distance([encodedTarget],faceEncoding[0])[0]
                if distance<= 0.3:
                    print(  image + " " + str(distance))
                    outputData["data"].append( image)
        
            # remove face files
            os.remove(facePath)
        
    writeToFile(resultFile)
    
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Target", help="Target path", required=True)
    parser.add_argument("-f", "--Folder", help="Image folder(end with '/')", required=True)
    args = parser.parse_args()

    findFace(args.Target, args.Folder)
