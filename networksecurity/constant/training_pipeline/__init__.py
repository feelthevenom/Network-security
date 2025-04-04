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
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str ="report.yaml"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocess.pkl"

SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"


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


"""
Data Transformation contants 
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transforamtion"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
## KNN imputer params
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

"""
Model Training Configutation
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD: float = 0.05