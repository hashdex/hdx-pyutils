import logging
from .datalake_manager import *
from .s3_manager import *
from .dynamodb_manager import *
from .inoa_api_manager import *
from .secrets_manager import *
from .lambda_manager import *

logging.basicConfig(format='%(asctime)s (%(levelname)s): %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

def set_log_level(level:str='NOTSET'):
    logging.root.setLevel(level) # NOTSET | DEBUG | INFO | WARNING | ERROR | CRITICAL