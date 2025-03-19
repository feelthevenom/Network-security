import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()

MONOGO_DB_URL = os.getenv('MONGO_DB_URL')  

# Certifi is a Python package that provides Mozilla's CA Bundle.
# It is used to validate the authenticity of SSL certificates while making HTTPS requests.
import certifi
ca = certifi.where() #ca = certificate authority

import pandas as pd
import numpy as np
import pymongo

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

logger = logging.getLogger('push_data')



class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,csv_file_path:str):
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True,inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records
    
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.records  = records
            self.collection = collection

            self.mongo_client = pymongo.MongoClient(MONOGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(records)
            logger.info('Data inserted successfully')

            return (len(self.records))
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == '__main__':
    FILE_PATH = os.path.join("Network_Data","phisingData.csv")
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"

    print('Pushing data to MongoDB')

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(FILE_PATH)

    print(records)

    no_of_records = networkobj.insert_data_mongodb(records,DATABASE,COLLECTION)

    print(f'{no_of_records} records inserted successfully')