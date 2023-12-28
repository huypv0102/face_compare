import argparse
import findfacev2
import face_recognition
import sys
import pickle
import dbhelper
import json

OUTPUTFILE = "model.txt"

def train(classId, images, dbUri, dbName, dbCollection) ->None:
    db=dbhelper.connect(dbUri,dbName)
    model = "cnn"
    #images = findfacev2.listAllImage(trainFolders)
    for filepath in images:
        name = filepath.split("\\")[-1].split(".")[0].split("_")[0] #123_name.jpg
        print(filepath)
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # 1 face
        if len(face_encodings) != 0:
            print("Traninig " + name)
            name_encoding = {"classId": int(classId), "studentId":int(name),"data":face_encodings[0].tolist()} 
            
            # check model not exist
            doc = db[dbCollection].find({"studentId":int(name)})
            if len(list(doc)) == 0:
                # then insert
                db[dbCollection].insert_one(name_encoding)
            else:
                # else
                query = { "studentId": int(name) }
                newvalues = { "$set": {"classId": int(classId), "data": name_encoding["data"] } }
                db[dbCollection].update_one(query,newvalues)
        else:
            print("No face in " + name)

    



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--Group", help="Student Group (classId)", default="123")
    parser.add_argument("-f", "--Files", nargs='+', help="Image files",  default='C:\\Users\\HUY-PC\\Desktop\\TestFaceRecognite\\117-SteamArt\\17302_LE_HA_NGOC_AI.jpg')
    parser.add_argument("-s", "--DBString", help="DB connection string", default="mongodb://awedev:awedev123@103.147.186.116:27017/?authMechanism=DEFAULT&authSource=CYC_Dev")
    parser.add_argument("-n", "--DBName", help="DB name", default="CYC_Dev")
    parser.add_argument("-c", "--DBCol", help="DB collection", default="FaceModels_huy")
    args = parser.parse_args()
        
    train(args.Group, args.Files,args.DBString,args.DBName,args.DBCol)
    
