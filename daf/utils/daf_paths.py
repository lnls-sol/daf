import os
from os import path

HOME = os.getenv("HOME")
SCAN_UTILS_USER_PATH = path.join(HOME, '.config/scan-utils/')
DEFAULT_SCAN_UTILS_CONFIG = path.join(SCAN_UTILS_USER_PATH, 'config.yml')
DAF_CONFIGS = path.join(HOME,".daf")
