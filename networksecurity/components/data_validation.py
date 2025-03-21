import os
import sys
import pandas as pd


from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig

#For train and test directry 
from networksecurity.entity.artifact_entity import DataIngetionArtifact, DataValidationArtifact

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp



logger = logging.getLogger('Data_Validation')


class DataValidation:
    def __init__(self,data_ingetion_artifact:DataIngetionArtifact,
                 datavalidationconfig:DataValidationConfig):
        try:
            self.data_ingetion_artifact=data_ingetion_artifact
            self.data_validation_config=datavalidationconfig
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_column(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logger.info(f"Required number of columns: {number_of_columns}")
            logger.info(f"Number of columns in dataframe: {len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error in validate_number_column: {e}")
            raise NetworkSecurityException(e)
        
        
    def find_numerical_column(self, dataframe:pd.DataFrame)->bool:
        try:
            return any(dataframe[col].dtype in ['int64', 'float64'] for col in dataframe.columns)
        except Exception as e:
            logger.error(e)
            raise NetworkSecurityException(e,sys)
        
    def detect_dataset_drift(self, base_df, currect_df, threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = currect_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column:{
                            "p_value":float(is_same_dist.pvalue),
                            "drift_status":is_found
                        }
                    }
                )
            drift_report_path = self.data_validation_config.data_dirft_report_dir

            # Create directry
            dir_path = os.path.dirname(drift_report_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_path, content=report, replace=False)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self) -> DataIngetionArtifact:
        try:
            train_file_path = self.data_ingetion_artifact.train_file_path
            test_file_path = self.data_ingetion_artifact.test_file_path

            ## Read the data from the train and test for validation
            logger.info("Reading the train and test data")

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## validate number of columns 
            status = self.validate_number_column(dataframe = train_dataframe)
            if not status:
                logger.error("Train dataframe does not contain all columns")
                error_message=f"Train dataframe does not contain all columns"
            status = self.validate_number_column(dataframe = test_dataframe)
            if not status:
                logger.error("Test dataframe does not contain all columns")
                error_message=f"Test dataframe does not contain all columns"    

            ## Find numeical data from column
            logger.info("Finding the data Frame contains numerical data or not")

            train_is_num = self.find_numerical_column(dataframe=train_dataframe)
            if not train_is_num:
                logger.info(f"{train_is_num} No numerical value have been found in Training")
            
            test_is_num = self.find_numerical_column(dataframe=test_dataframe)
            if not test_is_num:
                logger.info(f"{test_is_num} No numerical value have been found in Training")

            ## Check data Drift
            status = self.detect_dataset_drift(base_df=train_dataframe,currect_df=test_dataframe)

            dirr_path = os.path.dirname(self.data_validation_config.data_valid_train_dir)
            os.makedirs(dirr_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.data_valid_train_dir, index= False, header = True
            )

            test_dataframe.to_csv(
                self.data_validation_config.data_valid_test_dir, index= False, header = True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingetion_artifact.train_file_path,
                valid_test_file_path= self.data_ingetion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path= self.data_validation_config.data_dirft_report_dir

            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


