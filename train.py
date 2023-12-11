import argparse
import findfacev2
import face_recognition
import sys
import pickle
import dbhelper
import json

OUTPUTFILE = "model.txt"

def train(trainFolders, dbUri, dbName, dbCollection) ->None:
    db=dbhelper.connect(dbUri,dbName)
    model = "hog"
  
    images = findfacev2.listAllImage(trainFolders)
    for filepath in images:
        name = filepath.split("\\")[-1].split(".")[0]
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # 1 face
        if len(face_encodings) != 0:
            print("Traninig " + name)
            name_encoding = {"name":name,"data":face_encodings[0].tolist()} 
            
            # check model not exist
            doc = db[dbCollection].find({"name":name})
            if len(list(doc)) == 0:
                # then insert
                db[dbCollection].insert_one(name_encoding)
            else:
                # else
                query = { "name": name }
                newvalues = { "$set": { "data": name_encoding["data"] } }
                db[dbCollection].update_one(query,newvalues)
        else:
            print("No face in " + name)

    



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--Folder", help="Train folder(end with '/')", required=True)
    parser.add_argument("-s", "--DBString", help="DB connection string", required=True)
    parser.add_argument("-n", "--DBName", help="DB name", default="face_rec")
    parser.add_argument("-c", "--DBCol", help="DB collection", default="model")
    args = parser.parse_args()
        
    train(args.Folder,args.DBString,args.DBName,args.DBCol)
    
