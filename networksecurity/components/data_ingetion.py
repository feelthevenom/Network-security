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
from networksecurity.entity.artifact_entity import DataIngetionArtifact

logger = logging.getLogger('Data_Ingetion_Stage')


class DataIngetion:
    def __init__(self, data_ingestion_config: DataIngetionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e, sys)
        
    def export_collecton_as_dataframe(self):
        try:
            logger.info("Export the Collection from Mongo to DataFrame")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df.drop(columns=['_id'], inplace=True)
            
            df.replace({"na":np.nan}, inplace=True)
            logger.info("Exported the dataFrame from collection")
            return df

        except Exception as e:
            logger(e)
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logger.info("Eporting the dataFrame into feature store as raw data")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #Create the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logger.info(f"Feature store is stored in {feature_store_file_path}")

            return dataframe
        
        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e,sys)
        

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logger.info("Splitting the feature store dataFrame into train and test data")

            train_set,test_set = train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
                )

            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)

            logger.info("Creating both train and test directory")

            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)

            logger.info(f"Created training folder path {train_dir_path}")
            logger.info(f"Created testing folder path {test_dir_path}")

            # Continue from here
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )

            logger.info("Successfully save the training and testing data in to the folder")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingetion(self):
        try:
            dataframe = self.export_collecton_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingetionartifact=DataIngetionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
                )
            
            return dataingetionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)