# main file
import os.path
import subprocess

import toml

import dataset_converter

with open('config.toml', 'r') as f:
    config = toml.load(f)

# locations of the algorithms
btrblocks_location = "~/prj/BtrBlocks/build/my_compression"  # compiled program
elf_location = "~/prj/ELF/out/artifacts/start_compress_jar/start-compress.jar"  # jar location
buff_location = "~/prj/BUFF/database"  # location of the database directory in BUFF

result_list = [["Dataset", "Algorithm", "Compression Factor", "Compression Speed in μs", "Decompression Speed in μs"]]

for x in range(config["datasets"]["count_d"]):
    current_dataset = config["datasets"][str(x)]
    fl = dataset_converter.create_file_location(current_dataset)
    # convert datasets if it wasn't yet
    dataset_variations = len([name for name in os.listdir("./Datasets/" + current_dataset)])
    if dataset_variations == 1:
        dataset_converter.create_other_datasets(current_dataset, config["datasets"][str(x) + "_base"])
        print("successfully converted " + current_dataset)
    else:
        print(current_dataset + " was already converted")

    for y in range(config["algorithms"]["count_a"]):
        current_algorithm = config["algorithms"][str(y)].lower()

        # put together the execute string
        execute_string = ""
        match current_algorithm:
            case "btrblocks":
                execute_string += btrblocks_location + " " + fl + ".double"
            case "elf" | "chimp" | "gorilla" | "xz" | "snappy" | "brotli" | "zstd" | "fpc":
                execute_string += "java -jar " + elf_location + " " + current_algorithm + " " + fl + ".csv"
            case "buff":
                execute_string += ("cargo +nightly run --manifest-path " + buff_location +
                                   "/Cargo.toml --release  --package buff --bin comp_profiler " +
                                   fl + " buff 10000 1.1509")

        # execute the algorithm
        subprocess.run(execute_string, shell=True, capture_output=True)

        # collect the stats from the execution
        stats = [current_dataset, current_algorithm,
                 dataset_converter.read_numbers("./results/" + current_algorithm + ".csv", ",")]
        result_list.append(stats)

        print("successfully executed " + current_algorithm + " with dataset " + current_dataset + "\n")

# write the stats to a result file
with open("./results/results.csv", mode="w", encoding="utf-8") as file:
    for stats in result_list:
        for element in stats:
            if isinstance(element, str):
                file.write(element + "\t")
            else:
                for n in range(len(element)):
                    file.write(element[n] + "\t")
        file.write("\n")
