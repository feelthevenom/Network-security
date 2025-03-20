#networksecurity/constant/training_pipeline/__init__.py

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


"""
Data Ingetion related constants should be added here with DATA_INGESTION VAR NAME
"""

DATA_INGETTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGETTION_DATABASE_NAME: str = "NetworkSecurity"
DATA_INGETTION_DIR_NAME: str ="data_ingestion"
DATA_INGETTION__FEATURE_STORE_DIR: str = "feature_store"
DATA_INGETTION_INGESTED_DIR: str = "ingested"
DATA_INGETTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
