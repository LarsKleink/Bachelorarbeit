# main file
import toml
import subprocess
from dataset_converter import *
import os, os.path

with open('config.toml', 'r') as f:
    config = toml.load(f)

btrblocks_location = "~/prj/BtrBlocks/build/my_compression"
elf_location = chimp_location = gorilla_location = "~/prj/ELF/out/artifacts/start_compress_jar/start-compress.jar"
buff_location = "~/prj/BUFF/database"

for x in range(config["datasets"]["count_d"]):
    current_dataset = config["datasets"][str(x)]
    print(current_dataset)

    dataset_variations = len([name for name in os.listdir("./Datasets/" + current_dataset)])
    if dataset_variations == 1:
        create_other_datasets(current_dataset, config["datasets"][str(y) + "_base"])
        print("successfully converted dataset")
    else:
        print("dataset was already converted")

    for y in range(config["algorithms"]["count_a"]):
        current_algorithm = config["algorithms"][str(y)].lower()
        fl = create_file_location(current_dataset)
        execute_string = ""

        match current_algorithm:
            case "btrblocks":
                execute_string += btrblocks_location + " " + fl + ".double"
            case "elf":
                execute_string += "java -jar " + elf_location + " elf " + fl + ".csv"
            case "chimp":
                execute_string += "java -jar " + elf_location + " chimp " + fl + ".csv"
            case "gorilla":
                execute_string += "java -jar " + elf_location + " gorilla " + fl + ".csv"
            case "buff":
                execute_string += "cargo +nightly run --manifest-path " + buff_location + "/Cargo.toml --release  --package buff --bin comp_profiler " + fl + " buff 10000 1.1509"

        print(execute_string)
        subprocess.run(execute_string, shell=True, capture_output=True)
        print("successfully executed " + current_algorithm + " with dataset " + current_dataset + "\n")


# subprocess.run("~/prj/BtrBlocks/btrblocks/build/my_compression ~/prj/BtrBlocks/btrblocks/datasets/BUFF-datasetbin", shell=True)
# cargo run --manifest-path /home/lars/prj/BUFF/database/Cargo.toml --bin comp_profiler
# cargo +nightly run --manifest-path /home/lars/prj/BUFF/database/Cargo.toml --release  --package buff --bin comp_profiler ./data/randomwalkdatasample1k-1k buff-simd 10000 1.1509

