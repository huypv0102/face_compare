import os,shutil
import face_recognition
import extractface
import validateface

def findFace(target,imageFolder):

    if not validateface.validateFace(target):
        print("No valid face")
    else:
        target = face_recognition.load_image_file(target)
        encodedFace = face_recognition.face_encodings(target)[0]

        extractedFaceParentFolder = "extractedImages/"
        if not os.path.exists(extractedFaceParentFolder):
            os.makedirs(extractedFaceParentFolder) 
        # Extract faces from imageFolder to extractedFaceParentFolder
        extractface.extractFaceToFolder(imageFolder,extractedFaceParentFolder)
        extractedFaceFolders = os.listdir(extractedFaceParentFolder)

        for folder in extractedFaceFolders:
            files = os.listdir(extractedFaceParentFolder+folder)
            for file in files:
                facePath = extractedFaceParentFolder + folder + "/" +file
                face = face_recognition.load_image_file(facePath)
                faceEncoding = face_recognition.face_encodings(face)

                if len(faceEncoding) == 0:
                    continue

                distance = face_recognition.face_distance([encodedFace],faceEncoding[0])
                if distance[0]<= 0.33:
                    print( imageFolder + folder + " " + str(distance))
            
            # remove face folder
            shutil.rmtree(extractedFaceParentFolder+folder)

findFace("images/kid77.png","D:/face_reg/face_compare/images/")