#!/usr/bin/env python

import os.path
import subprocess
import time
import sqlite3
import argparse

import toml

import dataset_converter
import utils

NEW_RESULT_FILE_DEFAULT = True

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config", help="path to a toml-file")
    parser.add_argument("-a", "--algorithms", help="ALGORITHM_DATABASE: path to sqlite database")
    parser.add_argument("-e", "--execute_list", nargs="+", help="list of algorithms that should be tested")
    parser.add_argument("-d", "--datasets", nargs="+", help="list of datasets to test")
    parser.add_argument("-r", "--results_file", help="save results in default file or create a new one",
                        default=NEW_RESULT_FILE_DEFAULT)

    args = parser.parse_args()

    if args.config is None and args.algorithms is None and args.datasets is None:
        args.config = "config.toml"

    if args.algorithms is not None and args.datasets is not None:
        algorithms_location = args.algorithms

        # connect to the algorithms database
        connection = sqlite3.connect(algorithms_location)
        cursor = connection.cursor()

        full_algorithm_list = []
        for row in cursor.execute("SELECT name FROM algorithms"):
            full_algorithm_list.append(row[0])

        connection.close()

        if args.execute_list:
            execute_list = args.execute_list
        else:
            execute_list = full_algorithm_list
        datasets = args.datasets
        new_result_file = args.results_file
    else:
        with open(args.config, 'r') as f:
            config = toml.load(f)
        algorithms_location = config["algorithms_location"]
        execute_list = config["execute_list"]
        datasets = config["datasets"]
        new_result_file = config.get("new_result_file", NEW_RESULT_FILE_DEFAULT)

    result_list = [["Dataset", "Algorithm", "Compression Factor", "Compression Speed in μs",
                    "Decompression Speed in μs", "Execution time in seconds"]]

    project_location = utils.get_project_root()

    # connect to the algorithms database
    con = sqlite3.connect(algorithms_location)
    cur = con.cursor()

    for dataset in datasets:
        fl = utils.create_dataset_location(project_location, dataset)

        # convert dataset if it wasn't yet
        match utils.check_existing_datasets(dataset):
            case 1:         # binary, csv and buff exist
                pass
            case 2:         # binary and csv exist
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + dataset + " to buff-version\n")
            case 3:         # binary and buff exist
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + dataset + " to csv-version\n")
            case 4:         # only binary exists
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + dataset + " to csv-version\n")
            case 5:         # only csv exists
                dataset_converter.create_other_dataset(fl, "csv", "buff")
                print("converted " + dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + dataset + " to binary-version\n")
            case 6:         # csv and buff exist
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + dataset + " to binary-version\n")
            case 7:         # only buff exists
                dataset_converter.create_other_dataset(fl, "buff", "bin")
                print("converted " + dataset + " to binary-version")
                dataset_converter.create_other_dataset(fl, "buff", "csv")
                print("converted " + dataset + " to csv-version\n")

        for exec in execute_list:
            # get plugin, location and filetype from database
            query_result = cur.execute("SELECT plugin, location, file FROM algorithms WHERE name='" + exec + "'")
            exec_plugin, exec_location, exec_file = query_result.fetchone()

            # dynamically import the needed plugin
            module = utils.load_module("plugins/" + exec_plugin)

            # create the execute string with the correct plugin
            execute_string = module.create_execute_string(fl, exec_location, exec_file)
            # execute the algorithm
            start = time.time()
            subprocess.run(execute_string, shell=True, capture_output=True)
            length = time.time() - start
    
            # collect the stats from the execution if the execution was successful
            if time.time() - os.path.getmtime("./results/algorithms/" + exec + ".csv") < 2:
                stats = [dataset, exec, dataset_converter.read_numbers(
                    "./results/algorithms/" + exec + ".csv", ","), str(length)]
                print("successfully executed " + exec + " with dataset " + dataset + "\n")
                result_list.append(stats)
            else:
                stats = [dataset, exec, "error"]
                print("error at execution of " + exec + " with dataset " + dataset + "\n")
                result_list.append(stats)

    # close connection to the database
    con.commit()
    con.close()

    # check if a new file should be created or to write in the default file
    if new_result_file:
        result_file_path = "./results/results_" + time.strftime("%Y%m%d-%H%M%S").strip() + ".csv"
    else:
        result_file_path = "./results/results.csv"

    # write the stats to the result file
    with open(result_file_path, mode="w", encoding="utf-8") as file:
        for stats in result_list:
            for element in stats:
                if isinstance(element, str):
                    file.write(element + ",")
                else:
                    for n in range(len(element)):
                        file.write(element[n] + ",")
            file.write("\n")
