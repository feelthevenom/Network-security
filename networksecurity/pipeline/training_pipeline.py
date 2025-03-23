import sys,os

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#Data Ingetion
from networksecurity.components.data_ingetion import DataIngetion
#Data Validation
from networksecurity.components.data_validation import DataValidation
#Data Transformation
from networksecurity.components.data_transformation import DataTransformation
# Model Training
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngetionConfig, 
    DataValidationConfig, 
    DataTransformationConfig, 
    ModelTrainingConfig)

from networksecurity.entity.artifact_entity import (
    DataIngetionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainingArtifact
)

logger = logging.getLogger('Training_Pipeline')

class TrainPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingetion(self)->DataIngetionArtifact:
        try:
            self.data_ingetion_config = DataIngetionConfig(training_pipeline_config=self.training_pipeline_config)
            logger.info("Started Data ingetion")

            data_ingetion = DataIngetion(data_ingestion_config = self.data_ingetion_config)
            data_ingetion_artifact = data_ingetion.initiate_data_ingetion()
            logger.info("Data Ingetion is successfully completed")

            return data_ingetion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self, data_ingetion_artifact:DataIngetionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingetion_artifact,data_validation_config)
            
            logger.info("Data Validation is Initiated!")

            data_validation_artifact = data_validation.initiate_data_validation()

            logger.info("Data Validation is successfully done")

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transforamtion(self, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            logger.info("Data Tranformation is started beginning")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)

            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)

            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logger.info("Data Transformation is sucessfully done")

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_model_train(self, data_transformation_artifact: DataTransformationArtifact)->ModelTrainingArtifact:
        try:
            logger.info("Model Training part is initiated")

            model_trainer_config = ModelTrainingConfig(self.training_pipeline_config)

            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logger.info("Model is successfully trained and chosen best model and also tracked using mlflow")

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingetion_artifact = self.start_data_ingetion()
            data_validation_artifact = self.start_data_validation(data_ingetion_artifact = data_ingetion_artifact)
            data_transforamtion_artifact = self.start_data_transforamtion(data_validation_artifact = data_validation_artifact)
            model_trainer_artifact = self.start_model_train(data_transformation_artifact = data_transforamtion_artifact)

            return model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)