from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from . import app
from Thrive_Mind_App.auth import token_required, create_token
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


@app.route('/createnewdb', methods=['GET', 'POST'])
def createDatabase():
    # Construct connection string
    config = {
        'host':'thriveminddb.mysql.database.azure.com',
        'user':'thriveadmin@thriveminddb',
        'password':'Cmpt4741!',
        'database':'thriveminddb',
        'ssl_ca':'/Users/emleechxn/Downloads/BaltimoreCyberTrustRoot.crt.pem'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

         # Drop previous table of same name if one exists
        cursor.execute("DROP TABLE IF EXISTS patient;")
        print("Finished dropping PATIENT table (if existed).")

        # Create patient table
        cursor.execute("CREATE TABLE patient (user_id serial PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), user_name VARCHAR(50), user_password VARCHAR(50), email_address VARCHAR(50), phone VARCHAR(50), is_seeking BOOLEAN, medical_history VARCHAR(50), current_prescription VARCHAR(50), preferences VARCHAR(50), health_care_plan VARCHAR(50));")
        print("Finished creating PATIENT table.")

        # Drop previous table of same name if one exists
        cursor.execute("DROP TABLE IF EXISTS MOA;")
        print("Finished dropping MOA table (if existed).")
        
        # # Create MOA table
        # cursor.execute("CREATE TABLE MOA (user_id serial PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), user_name VARCHAR(50), user_password VARCHAR(50));")
        # print("Finished creating MOA table.")

        # # Drop previous table of same name if one exists
        # cursor.execute("DROP TABLE IF EXISTS clinic;")
        # print("Finished dropping clinic table (if existed).")

        # # Create CLINIC table
        # cursor.execute("CREATE TABLE clinic (clinic_id serial PRIMARY KEY, Physicians VARCHAR(50), phone VARCHAR(50), email VARCHAR(50), is_accepting BOOLEAN, list_of_services VARCHAR(50),hours VARCHAR(50), description VARCHAR(50), health_care_coverage VARCHAR(50));")
        # print("Finished creating clinic table.")

        # # Insert some prelim data into table (remove later)
        # cursor.execute("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, isSeeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"))
        # print("Inserted",cursor.rowcount,"row(s) of data.")

        # cursor.execute("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, isSeeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"))
        # print("Inserted",cursor.rowcount,"row(s) of data.")

        # cursor.execute("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, isSeeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"))
        
        print("Inserted",cursor.rowcount,"row(s) of data.")
       
        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
    return ''


@app.route('/createnewuser', methods=['GET', 'POST'])
def create_new_user():
    config = {
        'host':'thriveminddb.mysql.database.azure.com',
        'user':'thriveadmin@thriveminddb',
        'password':'Cmpt4741!',
        'database':'thriveminddb',
        'ssl_ca':'/Users/emleechxn/Downloads/BaltimoreCyberTrustRoot.crt.pem'
    }
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
    
        cursor.execute("INSERT INTO patient (first_name, last_name, user_name, user_password,email_address, phone, isSeeking, medical_history, current_prescription, preferences, health_care_plan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ("Bob", "Smith", "bobsmith", "hunter12", "bob.smith@smith.com", "123-123-123", True, "Anxiety", "Xanax", "require hearing aid", "blue cross"))
        print("Inserted",cursor.rowcount,"row(s) of data.")

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
    return ''
        
    

