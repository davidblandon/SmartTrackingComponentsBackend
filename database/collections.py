from pymongo import MongoClient
from .database import db

component_collection = db['component']
car_collection = db['car']
maintenance_collection = db['maintenance']
session_collection = db['session']
test_collection = db['test']
user_collection = db['user']