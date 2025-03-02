import os, sys, json, certifi, pymongo
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongo(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records), "Records Inserted Successfully")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "NetworkData/PhisingData.csv"
    DATABASE = "NetworkSecurity"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json(FILE_PATH)
    print(records)
    no_of_records, message = networkobj.insert_data_to_mongo(records, DATABASE, Collection)
    print(no_of_records, message)