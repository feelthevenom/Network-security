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

        pass

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
                training_pipeline.FILE_NAME
            )

            # Artifacts/data_ingestion/train.csv
            self.training_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            # Artifacts/data_ingestion/test.csv
            self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.TEST_FILE_NAME
            )
            self.train_test_split_ratio: float = training_pipeline.DATA_INGETTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name: str = training_pipeline.DATA_INGETTION_COLLECTION_NAME
            self.database_name: str = training_pipeline.DATA_INGETTION_DATABASE_NAME

        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e,sys)