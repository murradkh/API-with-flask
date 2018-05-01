import pymongo
import os

class Database(object):
    URI= os.environ.get('DB-URI')
    Database=None

    @staticmethod
    def initilalize():
        client=pymongo.MongoClient(Database.URI)
        Database.Database=client.get_default_database()

    @staticmethod
    def insert(collection,data):
        Database.Database[collection].insert(data)

    @staticmethod
    def find(collection,query):
       return Database.Database[collection].find(query)

    @staticmethod
    def find_one(collection,query):
       return Database.Database[collection].find_one(query)
