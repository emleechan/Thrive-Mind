import mysql.connector
from mysql.connector import errorcode
from mysql import *


# Obtain connection string information from the portal
config = {
  'host':'thriveminddb.mysql.database.azure.com',
  'user':'thriveadmin@thriveminddb',
  'password':'Cmpt4741!',
  'database':'thriveminddb',
  'ssl_ca':'database/BaltimoreCyberTrustRoot.crt.pem'
}

class DatabaseService():
  def __init__(self):
    self.connect()

  def connect(self):
    self.db = mysql.connector.connect(**config)
    print("Connection established")
    return self.db

  def init_database(self):
    cursor = self.db.cursor()
    
    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS patient;")
    print("Finished dropping PATIENT table (if existed).")
    cursor.execute("DROP TABLE IF EXISTS healthcareservice;")
    print("Finished dropping HEALTHCARESERVICE table (if existed).")

    # Create patient table
    cursor.execute("CREATE TABLE patient (user_id serial PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), user_name VARCHAR(50) UNIQUE, user_password VARCHAR(50), email_address VARCHAR(50) UNIQUE, phone VARCHAR(50), is_seeking BOOLEAN, medical_history VARCHAR(50), current_prescription VARCHAR(50), preferences VARCHAR(50), health_care_plan VARCHAR(50));")
    print("Finished creating PATIENT table.")

    # Create healthcareservice table
    cursor.execute("CREATE TABLE healthcareservice (id serial PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), email_address VARCHAR(50), phone VARCHAR(50), is_accepting BOOLEAN);")
    print("Finished creating HEALTHCARESERVICE table.")

    # Insert some data into healthcareservice table
    cursor.execute("INSERT INTO healthcareservice (name, description, email_address, phone, is_accepting) VALUES (%s, %s, %s, %s, %s);", ("healthcareservice1", "This is a description of healthcare service 1", "service1@healthcare.com", "(101) 301-0485", True))
    print("Inserted",cursor.rowcount,"row(s) of data.")
    cursor.execute("INSERT INTO healthcareservice (name, description, email_address, phone, is_accepting) VALUES (%s, %s, %s, %s, %s);", ("healthcareservice2", "This is a description of healthcare service 2", "service2@healthcare.com", "(202) 321-2485", False))
    print("Inserted",cursor.rowcount,"row(s) of data.")
    cursor.execute("INSERT INTO healthcareservice (name, description, email_address, phone, is_accepting) VALUES (%s, %s, %s, %s, %s);", ("someotherservice", "This is a description of a different service", "service3@somethingelse.com", "(666) 666-6666", True))
    print("Inserted",cursor.rowcount,"row(s) of data.")

    # Cleanup
    self.db.commit()
    cursor.close()
    print("Done init database.")

  def execute_insert_query(self, query, params):
    cursor = self.db.cursor()
    cursor.execute(query, params)
    self.db.commit()
    result = cursor.rowcount
    cursor.close()
    return result
  
  def execute_select_query(self, query, params):
    cursor = self.db.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    cursor.close()
    return (row_headers, result)