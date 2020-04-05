from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from __init__ import app
from auth import token_required, create_token, token_decode
from mysql import *
import mysql.connector
from mysql.connector import errorcode
from database.DatabaseService import DatabaseService
import json
from flask import request
from flask import abort

import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson.json_util import dumps


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/unprotected')
def unprotected():
    return ''


@app.route('/login', methods=['POST'])
def login():
    db = DatabaseService()
    req_data = request.get_json()
    passwd = req_data['user_password']
    username = req_data['user_name']
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_name = %s;", (username,))
    if(len(matchingusers)==0):
        return 'User is not in DB', 400
    elif(passwd!=matchingusers[0][4]):
        return 'Wrong Password', 400
    else:
        return create_token(matchingusers[0][0])



@app.route('/profile', methods=['GET'])
def profile():
    db = DatabaseService()
    req_data = request.get_json()
    token = request.headers.get('x-access-token')
    encrpytDict = token_decode(token)
    user_idCheck = encrpytDict['user_id']
    row_headers, matchinguser = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_id = %s;", (user_idCheck,))
    jsonresult = json.dumps(dict(zip(row_headers,matchinguser[0])))
    return "{}".format(jsonresult)

@app.route('/createnewdb', methods=['POST'])
def createDatabase():
    db = DatabaseService()
    db.init_database()
    return 'SUCCESS'


@app.route('/register', methods=['POST'])
def create_new_user():
    db = DatabaseService()
    req_data = request.get_json()
    role = req_data['role']
    print(req_data)
    username = req_data['user_name']
    null ='null'
    row_headers, matchingusers = db.execute_select_query("SELECT user_id,  user_name, user_password FROM patient WHERE user_name = %s;", (username,))
    if (len(matchingusers)!= 0):
        return 'User exists', 400
    else:
        rowcount = db.execute_insert_query("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, is_seeking) VALUES (%s, %s, %s, %s, %s, %s, %s);",
        (req_data['first_name'],req_data['last_name'],username,req_data['user_password'],req_data['email_address'],req_data['phone'],req_data['is_seeking']))
    return "Inserted {} rows.".format(rowcount)

# DEBUGGING ENDPOINT
@app.route('/getuser/<userid>', methods=['GET'])
def get_user_by_id(userid):
    db = DatabaseService()
    row_headers, matchinguser = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_id = %s;", (userid,))
    jsonresult = json.dumps(dict(zip(row_headers,matchinguser[0])))
    return "{}".format(jsonresult)

# DEBUGGING ENDPOINT
@app.route('/getusers', methods=['GET'])
def get_users():
    db = DatabaseService()
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient LIMIT 20;", ())
    jsondata = []
    for user in matchingusers:
        jsondata.append(dict(zip(row_headers,user)))
    jsonresult = json.dumps(jsondata)
    return "{}".format(jsonresult)

@app.route('/createhealthservicedb', methods=['POST'])
def create_table_and_add():
    # Auth successful, lets get the data from the db
    db_name = "healthcareservice"
    host = os.getenv("thriveminddb.mongo.cosmos.azure.com")
    connection_uri = "mongodb://thriveminddb:3ZVHbEQKjE7AwuaAFW5fIosnK7F5lr9ECQj9WgMSrzft3TQps8EsluPUCbgB1TFwWnTq2dSjLDy6eZcQilIwFg==@thriveminddb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@thriveminddb@"
    client = MongoClient(connection_uri)

    try:
        info = client.server_info() # Forces a call.
    except ServerSelectionTimeoutError:
        print("server is down.")

    dblist = client.list_database_names()
    if "healthcareservice" in dblist:
        return "The database exists."
    else:
        db = client['healthcareservice']
        user_collection = db['hid']

        user_collection.insert([{"hid": "e8898c0e-0589-4918-b683-7dfd08940a42", "description": "This is where you go if you get seriously hurt :/", "is_accepting": True, "name": "Surrey Memorial Hospital", "phone": "(666) 666-6666", "email_address": "surreym@hospital.com"}, {"hid": "774bcecc-3f08-4fe9-b977-834d256f342c", "description": "This is a description of a different service", "is_accepting": True, "name": "someotherservice", "phone": "(666) 666-6666", "email_address": "service3@somethingelse.com"}, {"hid": "d7e1f752-bc3a-4350-affc-9211b5596b83", "description": "Fever? Headache? Shortness of breath? Come test yourself safely, here!", "is_accepting": False, "name": "COVID-19 Test Drive-Thru", "phone": "(604) 123-4567", "email_address": "covid19@humanityisdoomed.com"}, {"hid": "5d92d5f6-74db-44ee-9f1a-5f4fc99a862a", "description": "Going on vacation? Get your vac(cin)ations!", "is_accepting": True, "name": "Travel Medical Clinic", "phone": "(778) 434-3102", "email_address": "travelmedical@vaccinations.com"}, {"hid": "cfde0a10-b45b-4002-a2b3-c9df87718ac6", "description": "Don't settle for second-best public counseling from a school... go private!", "is_accepting": False, "name": "ABC Private Counseling", "phone": "(202) 321-2485", "email_address": "ABC@private.com"}, {"hid": "012fa2e0-8cd4-4d6e-ba43-38bfa07e3ac1", "description": "Don't listen to the media, get your state-sponsored 'facts' here!", "is_accepting": True, "name": "CoronaVirus Info Center", "phone": "(987) 654-2934", "email_address": "coronavirus@isnotreal.com"}, {"hid": "557e0802-7e57-4e71-b93c-3b262c287f41", "description": "This is a description of healthcare service 1", "is_accepting": True, "name": "healthcareservice1", "phone": "(101) 301-0485", "email_address": "service1@healthcare.com"}, {"hid": "fa3b3826-431a-4681-b8c3-24d95f71a83f", "description": "This is a description of healthcare service 2", "is_accepting": False, "name": "healthcareservice2", "phone": "(202) 321-2485", "email_address": "service2@healthcare.com"}, {"hid": "f0a97661-007a-4ed4-9c34-130a39541e66", "description": "Find a counselor today, covered by your student insurance, today!", "is_accepting": True, "name": "SFU Counseling", "phone": "(101) 301-0485", "email_address": "sfucounseling@sfu.ca"}])

        for user in user_collection.find():
            print(user)
        return "Database created."
    

@app.route('/services', methods=['GET'])
def health_services_get():
    print("Request headers:")
    print(request.headers)
    print("Azure secret header: ")
    
    # Going to require a special secret sent by our API gateway to auth this api, since we're exposed to public
    azure_secret_header = "not received"
    try:
        azure_secret_header = request.headers['X-Azure-Secret-Header']
    except KeyError:
        pass
    print(azure_secret_header)
    if azure_secret_header != "u7qYDHWs8dZsBFK5qGlgwnYN3LKQCETitejYbvBEEPEyxa0HR5Vk0FTAaZz4k0tEn1ktuz3hcO6vpvsYvgPKHSHkF1oi6WRBeKrLEPEyxa0HR5Vk0FTAaZz4":
        abort(403)

    # Auth successful, lets get the data from the db
    db_name = "healthcareservice"
    host = os.getenv("thriveminddb.mongo.cosmos.azure.com")
    connection_uri = "mongodb://thriveminddb:3ZVHbEQKjE7AwuaAFW5fIosnK7F5lr9ECQj9WgMSrzft3TQps8EsluPUCbgB1TFwWnTq2dSjLDy6eZcQilIwFg==@thriveminddb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@thriveminddb@"
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
        del user["_id"]
        services.append(user)
    jsonresult = json.dumps(services)
    resp = make_response(jsonresult)
    resp.headers['Content-Type'] = "application/json"
    return resp

@app.route('/services/search', methods=['GET'])
@token_required
def health_services_search():
    name = request.args.get('search')
    print('search', name)
    description = request.args.get('search')
    email = request.args.get('search')
    isAcceptingStr = request.args.get('search')

    query_wheres = []
    query_values = []
    if name is not None:
        query_wheres.append("name LIKE %s")
        query_values.append("%" + name + "%")
    if description is not None:
        query_wheres.append("description LIKE %s")
        query_values.append("%" + description + "%")
    # if email is not None:
    #     query_wheres.append("email LIKE %s")
    #     query_values.append("%" + email + "%")
    # if isAcceptingStr is not None:
    #     query_wheres.append("is_accepting LIKE %s")
    #     query_values.append("%" + isAcceptingStr + "%")
    if len(query_wheres) == 0:
        abort(404)

    query_wheres_str = " and ".join(query_wheres)

    queryStr = "SELECT id, name, description, email_address, phone, is_accepting FROM healthcareservice WHERE " + query_wheres_str + " LIMIT 20;"

    db = DatabaseService()
    row_headers, matchingservices = db.execute_select_query(queryStr, query_values)
    jsondata = []
    for service in matchingservices:
        jsondata.append(dict(zip(row_headers, service)))
    jsonresult = json.dumps(jsondata)

    resp = make_response(jsonresult)
    resp.headers['Content-Type'] = "application/json"

    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="80")