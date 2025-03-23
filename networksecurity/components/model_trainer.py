import os, sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainingArtifact
from networksecurity.entity.config_entity import ModelTrainingConfig


from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import save_numpy_array, load_numpy_array
from networksecurity.utils.main_utils.utils import evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

logger = logging.getLogger('Model_Training')

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainingConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Descision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "Adaboost": AdaBoostClassifier()
            }

            params = {
                "Descision Tree":{
                    'criterion':['gini','entropy', 'log_loss'],
                                  },
                "Random Forest": {
                    'n_estimators': [8,16,32,64,128,256],
                },
                "Gradient Boosting":{
                    'learning_rate': [0.1,0.01,0.001],
                    'subsample': [0.6,0.7,0.8,0.85,0.9],
                    'n_estimators': [8,16,32,64,128,256],
                },
                "Logistic Regression":{},
                "Adaboost":{
                    'learning_rate': [0.1,0.01,0.001],
                    'n_estimators': [8,16,32,64,128,256],
                }
            }
            model_report: dict = evaluate_models(x_train = x_train, y_train = y_train, x_test = x_test, y_test = y_test, 
                                                 models=models, params = params)
            
            # Best model score from dict
            best_model_score = max(sorted(model_report.values()))

            # Best model name 
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            logger.info(f"The Best model name is {best_model}")

            y_train_pred = best_model.predict(x_train)

            classificaton_train_metric = get_classification_score(y_true=y_train, y_pred= y_train_pred)

            y_test_pred = best_model.predict(x_test)

            classificaton_test_metric = get_classification_score(y_true=y_test, y_pred= y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_training_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok= True)

            network_model = NetworkModel(preprocess= preprocessor, model=best_model)

            save_object(self.model_training_config.trained_model_file_path, obj=NetworkModel)

            ## Model Trainer Artifact 
            model_trained_artifact = ModelTrainingArtifact(
                trained_model_file_path=self.model_training_config.trained_model_file_path,
                train_metric_artifact = classificaton_train_metric,
                test_metric_artifact = classificaton_test_metric
            )

            logger.info(f"Model trained Artifact: {model_trained_artifact}")

            return model_trained_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainingArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)