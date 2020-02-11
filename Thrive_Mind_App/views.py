from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from . import app
from auth import token_required, create_token
from mysql import *
import mysql.connector
from mysql.connector import errorcode



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

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'protected route!'})

@app.route('/protected/route')
@token_required
def get_token():
    return ''

@app.route('/login')
def login():
    return create_token()


@app.route('/database', methods=['GET', 'POST'])
def createDatabase():
    # Construct connection string
    config = {
        'host':'thriveminddb.mysql.database.azure.com',
        'user':'pythonuser@thriveminddb',
        'password':'thrivemindSqlAzure!',
        'database':'thriveminddb',
        'ssl_ca':'/Users/emleechxn/Downloads/BaltimoreCyberTrustRoot.crt.pem'
    }
    
    conn = mysql.connector.connect(**config)

    conn.close()


        # if request.method == "POST":
        #     details = request.form
        #     firstName = details['fname']
        #     lastName = details['lname']
        #     cur = mysql.connection.cursor()
        #     cur.execute("INSERT INTO Users(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        #     mysql.connection.commit()
        #     cur.close()
        #     return 'success'
        # return render_template('database.html')


