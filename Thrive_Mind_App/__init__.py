from flask import Flask  # Import the Flask class
from flask_cors import CORS

app = Flask(__name__)    # Create an instance of the class for our use
CORS(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

# flask alchemy URI config
#dialect+driver://username:password@host:port/database
#mysql://scott:tiger@localhost/mydatabase
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thriveadmin@thriveminddb:Cmpt474!@thriveminddb.mysql.database.azure.com/thriveminddb'



#current config setup
    #   config = {
    # 'host':'thriveminddb.mysql.database.azure.com',
    # 'user':'thriveadmin @thriveminddb',
    # 'password':'Cmpt4741!',
    # 'database':'thriveminddb'
    # }