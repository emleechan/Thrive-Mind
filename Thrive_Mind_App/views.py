from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from . import app
from Thrive_Mind_App.auth import token_required, create_token, plaintxt
from mysql import *
import mysql.connector
from mysql.connector import errorcode
from database.DatabaseService import DatabaseService
import json

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/unprotected')
def unprotected():
    return ''


@app.route('/login', methods=['GET'])
def login():
    db = DatabaseService()
    req_data = request.get_json()
    passwd = req_data['user_password']
    username = req_data['user_name']
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_name = %s;", (username,))
    if(len(matchingusers)==0):
        return 'User is not in DB'   
    elif(passwd!=matchingusers[0][4]):
        return 'Wrong Password'
    else:
        return create_token(matchingusers[0][0])



@app.route('/profile', methods=['GET'])
def profile():
    db = DatabaseService()
    req_data = request.get_json()
    token = request.headers.get('x-access-token')
    encrpytDict = plaintxt(token)
    user_idCheck = encrpytDict['user_id']
    print(user_idCheck)
    # userID = req_data['user_id']
    # passwd = req_data['user_password']
    row_headers, matchinguser = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_id = %s;", (user_idCheck,))
    jsonresult = json.dumps(dict(zip(row_headers,matchinguser[0])))
    return "{}".format(jsonresult)

@app.route('/createnewdb', methods=['POST'])
def createDatabase():
    db = DatabaseService()
    db.init_database()
    return 'SUCCESS'


@app.route('/createnewuser', methods=['POST'])
@token_required
def create_new_user():
    db = DatabaseService()
    req_data = request.get_json()
    username = req_data['user_name']
    row_headers, matchingusers = db.execute_select_query("SELECT user_id,  user_name, user_password FROM patient WHERE user_name = %s;", (username,))
    if (len(matchingusers)!= 0):
        return 'User exists'
    else:
        rowcount = db.execute_insert_query("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (req_data['first_name'],req_data['last_name'],username,req_data['user_password'],req_data['email_address'],req_data['phone'],req_data['is_seeking'],req_data['medical_history'],
        req_data['current_prescription'],req_data['preferences'],req_data['health_care_plan']))
    return "Inserted {} rows.".format(rowcount)
#  ("Bertha", "Ravenclaw", "bigbertha", "bitty", "bigbertha@hahoo.com", "223-333-323", True, "Being Old", "oxy", "require walking aid", "red cross")
# ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"),

@app.route('/getuser/<userid>', methods=['GET'])
@token_required
def get_user_by_id(userid):
    db = DatabaseService()
    row_headers, matchinguser = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_id = %s;", (userid,))
    jsonresult = json.dumps(dict(zip(row_headers,matchinguser[0])))
    return "{}".format(jsonresult)

@app.route('/getusers', methods=['GET'])
@token_required
def get_users():
    db = DatabaseService()
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient LIMIT 20;", ())
    jsondata = []
    for user in matchingusers:
        jsondata.append(dict(zip(row_headers,user)))
    jsonresult = json.dumps(jsondata)
    return "{}".format(jsonresult)

