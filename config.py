import os
#need to learn how to use the config.py setup
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://thriveadmin:Cmpt474!@thriveminddb.mysql.database.azure.com/thriveminddb'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False




    #   config = {
    # 'host':'thriveminddb.mysql.database.azure.com',
    # 'user':'thriveadmin @thriveminddb',
    # 'password':'Cmpt4741!',
    # 'database':'thriveminddb'
    # }