"""
This file used to write the configuation of all the process of directry path and other config
"""

from datetime import datetime
import os
import sys

from networksecurity.constant import training_pipeline

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACTS_DIR)

logger = logging.getLogger('Entity_Config')

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name, timestamp)
        self.timestamp: str=timestamp

class DataIngetionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):

        try:
            logger.info("Entering to Config for Data Ingetion")
            # Directory to store the data ingested

            # Artifacts/data_ingestion
            self.data_ingestion_dir: str = os.path.join(
                training_pipeline_config.artifacts_dir,
                training_pipeline.DATA_INGETTION_DIR_NAME
            )

            # Artifacts/data_ingestion/feature_store
            self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGETTION__FEATURE_STORE_DIR,
                training_pipeline.FILE_NAME
            )

            # Artifacts/data_ingestion/train.csv
            self.training_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGETTION_INGESTED_DIR,
                training_pipeline.TRAIN_FILE_NAME
            )

            # Artifacts/data_ingestion/test.csv
            self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGETTION_INGESTED_DIR,
                training_pipeline.TEST_FILE_NAME
            )
            self.train_test_split_ratio: float = training_pipeline.DATA_INGETTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name: str = training_pipeline.DATA_INGETTION_COLLECTION_NAME
            self.database_name: str = training_pipeline.DATA_INGETTION_DATABASE_NAME

        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e,sys)        

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir:str = os.path.join(
                training_pipeline_config.artifacts_dir,
                training_pipeline.DATA_VALIDATION_DIR_NAME
            )
            
            # Save the valid data
            self.data_validation_valid_dir:str = os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_VALID_DIR
            )

            # Saved the invalid data
            self.data_validation_invalid_dir:str = os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_INVALID_DIR
            )

            # Save the train and test of Valid Data
            self.data_valid_train_dir = os.path.join(
                self.data_validation_valid_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            self.data_valid_test_dir = os.path.join(
                self.data_validation_valid_dir,
                training_pipeline.TEST_FILE_NAME
            )

            # Saves the train and test of Invalid Data
            self.data_invalid_train_dir = os.path.join(
                self.data_validation_invalid_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            self.data_invalid_test_dir = os.path.join(
                self.data_validation_invalid_dir,
                training_pipeline.TEST_FILE_NAME
            )
            
            # Saves the driifted data
            self.data_dirft_report_dir:str = os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
            )
        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e,sys)
        
## Data Transformation
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
            self.data_transformed_train_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                                training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
            self.data_transformed_test_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                                     training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
            self.data_transformed_object_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                                       training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifacts_dir,training_pipeline.MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD