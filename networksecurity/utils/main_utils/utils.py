import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

logger = logging.getLogger('Utils')

def read_yaml_file(file_path: str) -> dict:
    try:
        logger.info(f"Reading the yaml file from the path {file_path}")
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(e)
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
        logger.info(f"numpy array is successfully saved on {dir_path}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys) 

def save_object(file_path: str, obj: object) -> None:
    try:
        logger.info("Trying to save the pickle file of object")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logger.info(f"Successfully saved the pickle file in {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file:
            print(file)
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model, para, cv =3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)