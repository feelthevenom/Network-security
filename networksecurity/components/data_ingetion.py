import sys
import os
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


## configiguaration of the Data Ingetion Config
from networksecurity.entity.config_entity import DataIngetionConfig


class DataIngetion:
    def __init__(self, data_ingestion_config: DataIngetionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def export_collecton_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "-id" in df.columns:
                df.drop(columns=['_id'], inplace=True)
            
            df.replace({"na":np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #Create the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_test_split_store(self, dataframe):
        try:
            train,test = train_test_split(train_size=self.data_ingestion_config.train_test_split_ratio)

            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)

            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)

            # Continue from here
            pass

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingetion(self):
        try:
            dataframe = self.export_collecton_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
        except Exception as e:
            raise NetworkSecurityException(e,sys)