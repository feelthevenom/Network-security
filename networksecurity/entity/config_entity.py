from datetime import datetime
import os

from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime('%Y%m%d%H%M%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_dir = training_pipeline.ARTIFACTS_DIR
        self.artifacts_dir = os.path.join(self.artifacts_dir, timestamp)
        self.timestamp = timestamp

        pass

class DataIngetionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):

        # Directory to store the data ingested
        # Artifacts/data_ingestion
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifacts_dir,
            training_pipeline.DATA_INGETTION_DIR_NAME
        )

        # Artifacts/data_ingestion/feature_store
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGETTION__FEATURE_STORE_DIR
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
        