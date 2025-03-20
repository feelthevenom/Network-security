import os
import sys
import pandas as pd


from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig

#For train and test directry 
from networksecurity.entity.artifact_entity import DataIngetionArtifact

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH

from networksecurity.utils.main_utils.utils import read_yaml_file

from scipy.stats import ks_2samp



logger = logging.getLogger('Data_Validation')


class DataValidation:
    def __init__(self,data_ingetion_artifact:DataIngetionArtifact,
                 datavalidationconfig:DataValidationConfig):
        try:
            self.data_ingetion_artifact=data_ingetion_artifact
            self.data_validation_config=datavalidationconfig
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


