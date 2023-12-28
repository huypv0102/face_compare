from collections import Counter
import os,shutil
import face_recognition
import argparse
import sys
import json
from tqdm import tqdm
import dbhelper
import validatefacev2
import numpy
import extractfacev2
from pathlib import Path

EXTRACTEDFOLDER = "extractedFolder/"
if not os.path.exists(EXTRACTEDFOLDER):
    os.makedirs(EXTRACTEDFOLDER) 

RESULTFILE = "result.txt"

def listAllImage(folder):
    imageFiles = []
    for x in Path(folder).iterdir():
        if x.is_file():
            imageFiles.append(str(x))
        
    return imageFiles

def writeToFile(fileName,outputData):
    with open(fileName, "w") as outputFile:
        json_object = json.dumps(outputData, indent=4)
        outputFile.write(json_object)


def findByStudentId(array,id):
    for a in array:
        if "studentId" not in a:
            return None
        if a["studentId"] == id:
            return a
    return None



def classifyImage(classId, imageFolders, dbString, dbName,dbModelCollection,dbResultCollection):
    db=dbhelper.connect(dbString,dbName)
    trainedModel = db[dbModelCollection].find({"classId": int(classId)})

    name = []
    knownEncoded = []
    for i in trainedModel:
        print(i["studentId"])
        name.append(int(i["studentId"]))
        # name.append(i["name"])
        knownEncoded.append(numpy.array(i["data"]))

    for folder in imageFolders:
        postId = os.path.basename(os.path.dirname(folder))
        imageFiles = listAllImage(folder)
        classifyOutput =[]
        for filePath in tqdm(imageFiles):
            extractfacev2.hogDetectFaces(str(filePath),EXTRACTEDFOLDER)
            
            for face in os.listdir(EXTRACTEDFOLDER):
                facePath = EXTRACTEDFOLDER  + face
                image = face_recognition.load_image_file(facePath)
                faceLocations = face_recognition.face_locations(image, model="hog")
                faceEncodings = face_recognition.face_encodings(image, faceLocations)

                if len(faceEncodings)!=0:
                    results = face_recognition.compare_faces(knownEncoded , faceEncodings[0], 0.32)

                for studentId,isMatch in zip(name, results):
                    if isMatch:
                        studentData = findByStudentId(classifyOutput,studentId)
                        if not studentData:
                            classifyOutput.append({"studentId":int(studentId),"images" :[str(filePath)]})
                        else:
                            studentData["images"] = list(set(studentData["images"] + [str(filePath)]))
                        # print(studentData["images"])
                        if studentData:
                            studentPhotos = list(set(studentData["images"]))
                            # if studentPhotos.count() > 0:
                            # print(studentPhotos)
                            db[dbResultCollection].insert_one({"postId": int(postId), "studentId":int(studentId), "studentPhotos": studentPhotos})

                os.remove(facePath)
        print(classifyOutput)
        # db[dbResultCollection].insert_one({"postId":postId,"studentPhotos":classifyOutput})

    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--Group", help="Student Group (classId)", default="123")
    parser.add_argument("-f", "--Folder", nargs='+', help="Image folders(end with '/')", default=['C:\\Users\HUY-PC\\Desktop\\TestFaceRecognite\\Posts\\85860\\'])
    parser.add_argument("-s", "--DBString", help="DB connection string", default="mongodb://awedev:awedev123@103.147.186.116:27017/?authMechanism=DEFAULT&authSource=CYC_Dev")
    parser.add_argument("-n", "--DBName", help="DB name", default="CYC_Dev")
    parser.add_argument("-mc", "--DBModelCol", help="DB model collection", default="FaceModels_huy")
    parser.add_argument("-rc", "--DBResultCol", help="DB result collection", default="StudentImages")
    args = parser.parse_args()
    classifyImage(args.Group, args.Folder, args.DBString, args.DBName, args.DBModelCol, args.DBResultCol)
   