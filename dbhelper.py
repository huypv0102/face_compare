import pymongo

def connect(uri, database):
    client = pymongo.MongoClient(uri)
    db = client[database]
    return db

def updateResult(oldData,newData,collection,query):
    data = list(set(oldData + newData))
    newvalues = { "$set": {"data":data} }

    collection.update_one(query,newvalues)


# client = pymongo.MongoClient("mongodb://awedev:awedev123@103.147.186.116:27017/?authMechanism=DEFAULT&authSource=CYC_Dev")

# for db in client.list_databases():
#     print(db)