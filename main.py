from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys

logger = logging.getLogger('main')


if __name__ == '__main__':
    logger.info('This is main.py')
    try:
        a = 10/0
        print(a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)