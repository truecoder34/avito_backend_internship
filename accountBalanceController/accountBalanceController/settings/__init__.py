import os
import json

CONFIG_FILE = 'C:\\Users\\vplotnik\\localTruecoderRepos\\avito_backend_internship\\.etc\\config.json'

try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
        config['PROD']
    from .production import *


except KeyError:
    from .development import *

SECRET_KEY = config['SECRET_KEY']
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY