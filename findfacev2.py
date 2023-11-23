import os,shutil
import face_recognition
import argparse
import extractface
import json
import validateface

outputData = {
    "data":[]
}


def findFace(target,imageFolder):

    if not validateface.validateFace(target):
        print("No valid face")
    else:
        outputData["data"].append(target)
        extractedFolder = "extractedImages/"
        resultFile = "result.txt"
        if not os.path.exists(extractedFolder):
            os.makedirs(extractedFolder) 
        

        target = face_recognition.load_image_file(target)
        encodedFace = face_recognition.face_encodings(target)[0]

        images = os.listdir(imageFolder)
        for image in images:
            extractface.extractFaceToFolder(imageFolder + image,extractedFolder)
            if os.path.exists(extractedFolder):
                extractedImages = os.listdir(extractedFolder )
            else:
                continue

            for extracted in extractedImages:
                facePath = extractedFolder  + extracted
                face = face_recognition.load_image_file(facePath)
                faceEncoding = face_recognition.face_encodings(face)

                
                if len(faceEncoding) != 0:
                    distance = face_recognition.face_distance([encodedFace],faceEncoding[0])
                    if distance[0]<= 0.33:
                        print( imageFolder + image + " " + str(distance))
                        outputData["data"].append(imageFolder + image)
            
                # remove face files
                os.remove(facePath)
        
        with open(resultFile, "w") as outputFile:
            json_object = json.dumps(outputData, indent=4)
            outputFile.write(json_object)

# findFace("D:/face_reg/UTKface_inthewild-20231121T025338Z-001/UTKface_inthewild/part1/part1/8_1_2_20170109203442372.jpg","D:/face_reg/UTKface_inthewild-20231121T025338Z-001/UTKface_inthewild/part1/part1/")
# findFace("images/hs.jpg", "images/")
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Target", help="Target path", required=True)
    parser.add_argument("-f", "--Folder", help="Image folder(end with '/')", required=True)
    args = parser.parse_args()

    findFace(args.Target, args.Folder)
