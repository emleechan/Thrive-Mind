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
        'user':'thriveadmin@thriveminddb',
        'password':'Cmpt4741!',
        'database':'users',
        'ssl_ca':'/Users/emleechxn/Downloads/BaltimoreCyberTrustRoot.crt.pem'
    }
    
    # conn = mysql.connector.connect(**config)
    # conn.close()
    # return ''

    # if request.method == "POST":
    #     details = request.form
    #     firstName = details['fname']
    #     lastName = details['lname']
    #     conn = mysql.connection.cursor()
    #     conn.execute("INSERT INTO Users(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
    #     mysql.connection.commit()
    #     conn.close()
    #     return 'success'
    # return render_template('database.html')
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
        cursor.execute("DROP TABLE IF EXISTS inventory;")
        print("Finished dropping table (if existed).")

        # Create table
        cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
        print("Finished creating table.")

        # Insert some data into table
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
        print("Inserted",cursor.rowcount,"row(s) of data.")
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
        print("Inserted",cursor.rowcount,"row(s) of data.")
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
        print("Inserted",cursor.rowcount,"row(s) of data.")

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
        return ''


