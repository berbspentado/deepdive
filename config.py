import os
from os.path import join,dirname #joining a path, and dirname is directory of filename
from dotenv import load_dotenv #for looking at env


dot_env = join(dirname(__file__),'.env')

class DevelopmentConfig():
    #to turn on debug mode of the flask
    DEBUG = True
    #setup sqlalchemy where to get db
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/deepdive?charset=utf8'.format(**{
        'user':os.environ.get('MYSQL_USER','root'),
        'password':os.environ.get('MYSQL_PASSWORD',''),
        'host':os.environ.get('DB_HOST','localhost'),

    })

    #connection for not failing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

Config = DevelopmentConfig   