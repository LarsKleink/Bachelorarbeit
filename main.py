# main file
import importlib.util
import secrets
import string
import sys
import os.path
import subprocess
import time

import toml

import dataset_converter


def gensym(length=32, prefix="gensym_"):
    """
    generates a fairly unique symbol, used to make a module name,
    used as a helper function for load_module

    :return: generated symbol
    """
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol


def load_module(source, module_name=None):
    """
    reads file source and loads it as a module

    :param source: file to load
    :param module_name: name of module to register in sys.modules
    :return: loaded module
    """

    if module_name is None:
        module_name = gensym()

    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


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


if __name__ == "__main__":
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    result_list = [["Dataset", "Algorithm", "Compression Factor", "Compression Speed in μs", "Decompression Speed in μs", "Execution time in seconds"]]

    algorithms = config["algorithms"]
    execute_list = config["execute"]
    datasets = config["datasets"]

    for x in range(len(datasets)):
        current_dataset = datasets[str(x)]
        fl = dataset_converter.create_file_location(current_dataset)

        # convert datasets if it wasn't yet
        match check_existing_datasets(current_dataset):
            case 1:         # binary, csv and buff exist
                pass
            case 2:         # binary and csv exist
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + current_dataset + " to buff-version")
            case 3:         # binary and buff exist
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + current_dataset + " to csv-version")
            case 4:         # only binary exists
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + current_dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + current_dataset + " to csv-version")
            case 5:         # only csv exists
                dataset_converter.create_other_dataset(fl, "csv", "buff")
                print("converted " + current_dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + current_dataset + " to binary-version")
            case 6:         # csv and buff exist
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + current_dataset + " to binary-version")
            case 7:         # only buff exists
                dataset_converter.create_other_dataset(fl, "buff", "bin")
                print("converted " + current_dataset + " to binary-version")
                dataset_converter.create_other_dataset(fl, "buff", "csv")
                print("converted " + current_dataset + " to csv-version")

        for exec in execute_list:
            algorithm = algorithms[exec]
            module = load_module("plugins/" + algorithm.get("plugin"))

            execute_string = module.create_execute_string(fl, algorithm.get("location"), algorithm.get("file"))
            # execute the algorithm
            start = time.time()
            subprocess.run(execute_string, shell=True, capture_output=True)
            end = time.time()
            length = (end - start) * 1
    
            # collect the stats from the execution
            stats = [current_dataset, exec,
                     dataset_converter.read_numbers("./results/algorithms/" + exec + ".csv", ","), str(length)]
            result_list.append(stats)
    
            print("successfully executed " + exec + " with dataset " + current_dataset + "\n")

    result_file_path = ""
    if config["new_result_file"] is True:
        result_file_path = "./results/results_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    else:
        result_file_path = "./results/results.csv"

    # write the stats to a result file
    with open("./results/results.csv", mode="w", encoding="utf-8") as file:
        for stats in result_list:
            for element in stats:
                if isinstance(element, str):
                    file.write(element + ",")
                else:
                    for n in range(len(element)):
                        file.write(element[n] + ",")
            file.write("\n")

