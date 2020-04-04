import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson.json_util import dumps



db_name = "healthcareservice"
host = os.getenv("thriveminddb.mongo.cosmos.azure.com")
port = 10255
username = os.getenv("thriveminddb")
password = os.getenv("3ZVHbEQKjE7AwuaAFW5fIosnK7F5lr9ECQj9WgMSrzft3TQps8EsluPUCbgB1TFwWnTq2dSjLDy6eZcQilIwFg==")
args = "ssl=true&retrywrites=false&ssl_cert_reqs=CERT_NONE"
connection_uri = "mongodb://thriveminddb:3ZVHbEQKjE7AwuaAFW5fIosnK7F5lr9ECQj9WgMSrzft3TQps8EsluPUCbgB1TFwWnTq2dSjLDy6eZcQilIwFg==@thriveminddb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@thriveminddb@"

# user_collection.insert_one({"email": "amer@foobar.com"})

def services_get(event, context):
    client = MongoClient(connection_uri)
    try:
        info = client.server_info() # Forces a call.
    except ServerSelectionTimeoutError:
        print("server is down.")
    db = client[db_name]
    # print(event)
    services = []
    user_collection = db['hid']
    for user in user_collection.find():
        #print(user)
        services.append(dumps(user))
    return services


