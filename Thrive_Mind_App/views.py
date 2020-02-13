from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from . import app
# from Thrive_Mind_App.auth import token_required, create_token
from mysql import *
import mysql.connector
from mysql.connector import errorcode
from database.DatabaseService import DatabaseService
import json

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

@app.route('/login')
def login():
    return create_token()


@app.route('/createnewdb', methods=['POST'])
def createDatabase():
    db = DatabaseService()
    db.init_database()
    return 'SUCCESS'


@app.route('/createnewuser', methods=['POST'])
def create_new_user():
    db = DatabaseService()
    rowcount = db.execute_insert_query("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, is_seeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"))
    return "Inserted {} rows.".format(rowcount)


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
