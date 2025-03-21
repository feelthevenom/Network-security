#networksecurity/constant/training_pipeline/__init__.py

"""
This constant contains the constant variable which more of an Pre define config
"""

import os
import sys
import numpy as np
import pandas as pd


"""
Define common constants variable for training pipeline
"""
TARGET_VARIABLE: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACTS_DIR: str = "Artifacts"
FILE_NAME: str = "PhisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")


"""
Data Ingetion related constants should be added here with DATA_INGESTION VAR NAME
"""

DATA_INGETTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGETTION_DATABASE_NAME: str = "NetworkSecurity"
DATA_INGETTION_DIR_NAME: str ="data_ingestion"
DATA_INGETTION__FEATURE_STORE_DIR: str = "feature_store"
DATA_INGETTION_INGESTED_DIR: str = "ingested"
DATA_INGETTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation constants should be added here with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str ="report.yaml"