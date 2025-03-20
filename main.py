import sys

from networksecurity.components.data_ingetion import DataIngetion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngetionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig 



if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()
        dataingetion_config = DataIngetionConfig(training_pipeline_config)
        dataingetion = DataIngetion(dataingetion_config)
        logging.info("Initial The data Ingetion")
        dataingetionartifact=dataingetion.initiate_data_ingetion()
        print(dataingetionartifact)



    except Exception as e:
        raise NetworkSecurityException(e,sys)