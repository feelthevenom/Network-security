import sys
import os
import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer

from networksecurity.entity.config_entity import DataTransformationConfig

from networksecurity.constant.training_pipeline import TARGET_VARIABLE, DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from networksecurity.utils.main_utils.utils import save_numpy_array, save_object

logger = logging.getLogger('Data_Transformation')

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transforamtion_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transforamtion_config: DataTransformationConfig = data_transforamtion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_tranformer_object(cls)->Pipeline:
        logger.info("Entered the data tranformater object method of transformation class")
        try:
            logger.info("Initiating KNN Imputer")
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline([("imputer",imputer)])

            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Entering the data transformation function")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df = train_df.drop(columns=[TARGET_VARIABLE], axis=True)
            target_feature_train_df = train_df[TARGET_VARIABLE]
            # contains -1 1 change to 0 1
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[TARGET_VARIABLE], axis=True)
            target_feature_test_df = test_df[TARGET_VARIABLE]
            # contains -1 1 change to 0 1
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_tranformer_object()
            preprocess_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocess_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocess_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array(self.data_transforamtion_config.data_transformed_train_file_path, array=train_arr)
            save_numpy_array(self.data_transforamtion_config.data_transformed_test_file_path, array=test_arr)
            save_object(self.data_transforamtion_config.data_transformed_object_file_path, preprocess_object)

            # save in final models
            save_object(os.path.join('final_model','preprocess.pkl'), preprocess_object)

            # prepare artifacts 
            data_tranformation_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transforamtion_config.data_transformed_object_file_path,
                transformed_train_file_path = self.data_transforamtion_config.data_transformed_train_file_path,
                transformed_test_file_path = self.data_transforamtion_config.data_transformed_test_file_path
            )

            return data_tranformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        