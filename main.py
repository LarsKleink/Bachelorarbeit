# main file
import os.path
import subprocess
import time

import toml

import dataset_converter


if __name__ == "__main__":
    with open('config.toml', 'r') as f:
        config = toml.load(f)

    result_list = [["Dataset", "Algorithm", "Compression Factor", "Compression Speed in μs",
                    "Decompression Speed in μs", "Execution time in seconds"]]

    algorithms = config["algorithms"]
    execute_list = config["execute"]
    datasets = config["datasets"]

    for x in range(len(datasets)):
        current_dataset = datasets[str(x)]
        fl = dataset_converter.create_file_location(current_dataset)

        # convert dataset if it wasn't yet
        match dataset_converter.check_existing_datasets(current_dataset):
            case 1:         # binary, csv and buff exist
                pass
            case 2:         # binary and csv exist
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + current_dataset + " to buff-version\n")
            case 3:         # binary and buff exist
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + current_dataset + " to csv-version\n")
            case 4:         # only binary exists
                dataset_converter.create_other_dataset(fl, "bin", "buff")
                print("converted " + current_dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "bin", "csv")
                print("converted " + current_dataset + " to csv-version\n")
            case 5:         # only csv exists
                dataset_converter.create_other_dataset(fl, "csv", "buff")
                print("converted " + current_dataset + " to buff-version")
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + current_dataset + " to binary-version\n")
            case 6:         # csv and buff exist
                dataset_converter.create_other_dataset(fl, "csv", "bin")
                print("converted " + current_dataset + " to binary-version\n")
            case 7:         # only buff exists
                dataset_converter.create_other_dataset(fl, "buff", "bin")
                print("converted " + current_dataset + " to binary-version")
                dataset_converter.create_other_dataset(fl, "buff", "csv")
                print("converted " + current_dataset + " to csv-version\n")

        for exec in execute_list:
            algorithm = algorithms[exec]

            # dynamically import the needed plugin
            module = dataset_converter.load_module("plugins/" + algorithm.get("plugin"))

            # create the execute string with the correct plugin
            execute_string = module.create_execute_string(fl, algorithm.get("location"), algorithm.get("file"))
            # execute the algorithm
            start = time.time()
            subprocess.run(execute_string, shell=True, capture_output=True)
            length = time.time() - start
    
            # collect the stats from the execution if the execution was successful
            if time.time() - os.path.getmtime("./results/algorithms/" + exec + ".csv") < 2:
                stats = [current_dataset, exec, dataset_converter.read_numbers(
                    "./results/algorithms/" + exec + ".csv", ","), str(length)]
                print("successfully executed " + exec + " with dataset " + current_dataset + "\n")
                result_list.append(stats)
            else:
                stats = [current_dataset, exec, "error"]
                print("error at execution of " + exec + " with dataset " + current_dataset + "\n")
                result_list.append(stats)

    # check if a new file should be created or to write in the default file
    if config["new_result_file"]:
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
