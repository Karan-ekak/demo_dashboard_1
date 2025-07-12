from os import path
import time


BASE_DIR=path.abspath(path.dirname(__file__))
LOGS_PATH=F'{BASE_DIR}/logs/'
# print(BASE_DIR)


def pendingUpload_path():
    return F"{BASE_DIR}/storage/pending_upload/"

def current_path():
    return F"{BASE_DIR}/"

def uploaded_path():
    return F"{BASE_DIR}/storage/uploaded/"

def logs_path():
    return F'{BASE_DIR}/logs/'
