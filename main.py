import sys

#Data Ingetion
from networksecurity.components.data_ingetion import DataIngetion
#Data Validation
from networksecurity.components.data_validation import DataValidation, DataValidationConfig

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngetionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig 

logger = logging.getLogger('Main')

if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        dataingetion_config = DataIngetionConfig(training_pipeline_config)
        dataingetion = DataIngetion(dataingetion_config)

        logger.info("Initial The data Ingetion")

        dataingetionartifact=dataingetion.initiate_data_ingetion()
        print(dataingetionartifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(dataingetionartifact,data_validation_config)
        
        logger.info("Data Validation is Initiated!")

        data_validation_artifact = data_validation.initiate_data_validation()

        logger.info("Data has been Successfully validated!")

        print(data_validation_artifact)




    except Exception as e:
        raise NetworkSecurityException(e,sys)