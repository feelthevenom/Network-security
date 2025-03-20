import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

logger = logging.getLogger('Utils')

def read_yaml_file(file_path: str) -> dict:
    try:
        logger.info(f"Reading the yaml file from the path {file_path}")
        with open(file_path, "rb") as file:
            return yaml.safe_load(yaml)
    except Exception as e:
        logger.error(e)
        raise NetworkSecurityException(e,sys)
