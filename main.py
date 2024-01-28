# main file
import toml
import subprocess
from dataset_converter import *
import os, os.path

with open('config.toml', 'r') as f:
    config = toml.load(f)

btrblocks_location = "~/prj/BtrBlocks/btrblocks/build/my_compression"
elf_location = chimp_location = gorilla_location = "./Algorithms/ELF/out/artifacts/start_compress_jar/start-compress.jar"
buff_location = "./Algorithms/BUFF"

for x in range(config["algorithms"]["count_a"]):
    current_algorithm = config["algorithms"][str(x)].lower()
    for y in range(config["datasets"]["count_d"]):
        current_dataset = config["datasets"][str(y)]
        print(current_dataset)
        fl = create_file_location(current_dataset)
        dataset_variations = len([name for name in os.listdir("./Datasets/" + current_dataset)])
        if dataset_variations == 1:
            create_other_datasets(current_dataset, config["datasets"][str(y) + "_base"])
            print("successfully converted dataset")
        else:
            print("dataset was already converted")
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
                execute_string += buff_location + " " + fl
        print(execute_string)
        subprocess.run(execute_string, shell=True)
        print("successfully executed " + current_algorithm + " with dataset " + current_dataset + "\n")



# subprocess.run("~/prj/BtrBlocks/btrblocks/build/my_compression ~/prj/BtrBlocks/btrblocks/datasets/BUFF-datasetbin", shell=True)
