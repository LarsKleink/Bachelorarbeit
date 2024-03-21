import importlib.util
import os
import secrets
import string
import sys

from pathlib import Path


def create_dataset_location(project_location: str, file_location: str):
    return project_location + "/Datasets/" + file_location + "/" + file_location


def check_existing_datasets(directory: str):
    path = "./Datasets/" + directory + "/" + directory
    if os.path.isfile(path + ".double") and os.path.isfile(path + ".csv") and os.path.isfile(path):
        return 1        # binary, csv and buff exist
    elif os.path.isfile(path + ".double") and os.path.isfile(path + ".csv") and not os.path.isfile(path):
        return 2        # binary and csv exist
    elif os.path.isfile(path + ".double") and not os.path.isfile(path + ".csv") and os.path.isfile(path):
        return 3        # binary and buff exist
    elif os.path.isfile(path + ".double") and not os.path.isfile(path + ".csv") and not os.path.isfile(path):
        return 4        # only binary exists
    elif os.path.isfile(path + ".csv") and not os.path.isfile(path):
        return 5        # only csv exists
    elif os.path.isfile(path + ".csv") and os.path.isfile(path):
        return 6        # csv and buff exist
    else:
        return 7        # only buff exists


def gen_sym(length=32, prefix="gen_sym_"):
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol


def load_module(source, module_name=None):
    if module_name is None:
        module_name = gen_sym()

    spec = importlib.util.spec_from_file_location(module_name, source)
    new_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = new_module
    spec.loader.exec_module(new_module)

    return new_module


def get_project_root():
    return str(Path(__file__).parent)
