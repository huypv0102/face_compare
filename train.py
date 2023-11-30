import argparse
import findfacev2
import face_recognition
import pickle


OUTPUTFILE = "model.pkl"

def train(trainFolder) ->None:
    model = "hog"
    names = []
    encodings = []
    images = findfacev2.listAllImage(trainFolder)
    for filepath in images:
        name = filepath.split("\\")[-1].split(".")[0]
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        # only 1 face
        if len(face_encodings) != 0:
            names.append(name)
            encodings.append(face_encodings[0])
        else:
            print("No face in " + name)

    name_encodings = {"names": names, "encodings": encodings}
    with open(OUTPUTFILE, "wb") as f:
        pickle.dump(name_encodings, f)


    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--Folder", help="Train folder(end with '/')", required=True)
    args = parser.parse_args()

    train(args.Folder)
    