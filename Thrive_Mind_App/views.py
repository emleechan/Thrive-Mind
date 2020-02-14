from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from . import app
from Thrive_Mind_App.auth import token_required, create_token
from mysql import *
import mysql.connector
from mysql.connector import errorcode
from database.DatabaseService import DatabaseService
import json
from flask import request
from flask import abort

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/unprotected')
def unprotected():
    return ''

# @app.route('/protected')
# @token_required
# def protected():
#     return jsonify({'message': 'protected route!'})

# @app.route('/protected/route')
# @token_required
# def get_token():
#     return ''

@app.route('/login', methods=['GET'])
def login():
    db = DatabaseService()
    username = 'bigbertha'
    passwd = "bitty"
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_name = %s;", (username,))
    if(len(matchingusers)==0):
        print('user doesnt exist')
        return 'User is not in DB'   
    elif(passwd!=matchingusers[0][4]):
        return 'Wrong Password'
    else:
        return create_token()


@app.route('/createnewdb', methods=['POST'])
def createDatabase():
    db = DatabaseService()
    db.init_database()
    return 'SUCCESS'


@app.route('/createnewuser', methods=['POST'])
def create_new_user():
    db = DatabaseService()
    # new_user =
    username = 'bigbertha' # case1 user exists
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_name = %s;", (username,))
    if (len(matchingusers)!= 0):
        return 'User exists'
    else:
        rowcount = db.execute_insert_query("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",)
    return "Inserted {} rows.".format(rowcount)
#  ("Bertha", "Ravenclaw", "bigbertha", "bitty", "bigbertha@hahoo.com", "223-333-323", True, "Being Old", "oxy", "require walking aid", "red cross")
# ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"),

@app.route('/getuser/<userid>', methods=['GET'])
def get_user_by_id(userid):
    db = DatabaseService()
    row_headers, matchinguser = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient WHERE user_id = %s;", (userid,))
    jsonresult = json.dumps(dict(zip(row_headers,matchinguser[0])))
    return "{}".format(jsonresult)

@app.route('/getusers', methods=['GET'])
def get_users():
    db = DatabaseService()
    row_headers, matchingusers = db.execute_select_query("SELECT user_id, first_name, last_name, user_name, user_password, email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan FROM patient LIMIT 20;", ())
    jsondata = []
    for user in matchingusers:
        jsondata.append(dict(zip(row_headers,user)))
    jsonresult = json.dumps(jsondata)
    return "{}".format(jsonresult)

@app.route('/services', methods=['GET'])
def health_services_get():
    db = DatabaseService()
    row_headers, matchingservices = db.execute_select_query("SELECT id, name, description, email_address, phone, is_accepting FROM healthcareservice LIMIT 20;", ())
    jsondata = []
    for service in matchingservices:
        jsondata.append(dict(zip(row_headers, service)))
    jsonresult = json.dumps(jsondata)

    resp = make_response(jsonresult)
    resp.headers['Content-Type'] = "application/json"

    return resp

@app.route('/services/search', methods=['GET'])
def health_services_search():
    name = request.args.get('name')
    description = request.args.get('description')
    email = request.args.get('email')
    isAcceptingStr = request.args.get('isAccepting')

    query_wheres = []
    query_values = []
    if name is not None:
        query_wheres.append("name LIKE %s")
        query_values.append("%" + name + "%")
    if description is not None:
        query_wheres.append("description LIKE %s")
        query_values.append("%" + description + "%")
    if email is not None:
        query_wheres.append("email LIKE %s")
        query_values.append("%" + email + "%")
    if isAcceptingStr is not None:
        query_wheres.append("is_accepting LIKE %s")
        query_values.append("%" + isAcceptingStr + "%")
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

