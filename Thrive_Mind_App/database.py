import mysql.connector
from mysql.connector import errorcode
from mysql import *


# Obtain connection string information from the portal
config = {
  'host':'thriveminddb.mysql.database.azure.com',
  'user':'thriveadmin @thriveminddb',
  'password':'Cmpt4741!',
  'database':'thriveminddb'
}

def db_init():
    try:
        db = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = db.cursor()
    return db

def create_database():
  db = db_init()
  cursor = db.cursor()
  
  # Drop previous table of same name if one exists
  cursor.execute("DROP TABLE IF EXISTS inventory;")
  print("Finished dropping table (if existed).")

  # Create table
#   cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
  cursor.execute("CREATE TABLE patient (user_id serial PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), user_name VARCHAR(50), user_password VARCHAR(50), email_address VARCHAR(50), phone VARCHAR(50), medical_history VARCHAR(50), current_prescription VARCHAR(50), preferences VARCHAR(50), health_care_plan VARCHAR(50));")
  print("Finished creating table.")

  # Insert some data into table
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
  print("Inserted",cursor.rowcount,"row(s) of data.")
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
  print("Inserted",cursor.rowcount,"row(s) of data.")
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
  print("Inserted",cursor.rowcount,"row(s) of data.")

  # Cleanup
  db.commit()
  cursor.close()
  db.close()
  print("Done.")