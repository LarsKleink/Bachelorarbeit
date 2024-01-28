import csv
import struct
from math import ceil
import binascii


def read_numbers(file_location: str, delimiter):
    numbers = []
    with open(file_location, mode="r", encoding="utf-8") as file:
        for line in file:
            line = line.split(delimiter)
            for i in range(len(line)):
                line[i].strip()
            numbers.extend(line)
    return numbers


def write_numbers(numbers: list[str], file_location: str, per_line: int):
    steps = ceil(len(numbers)/per_line)
    with open(file_location, mode="w", encoding="utf") as file:
        for step in range(steps):
            numbers_to_write = ",".join(numbers[step*per_line:step*per_line+per_line])
            file.write(str(numbers_to_write)+'\n')


def read_binary(file_location: str):
    numbers = []
    with open(file_location, mode="rb") as file:
        file_content = file.read().hex()
        print(len(file_content))
        for i in range(int(len(file_content)/16)):
            number_hex = file_content[i*16:(i+1)*16]
            numbers.append(str(struct.unpack('!d', bytes.fromhex(number_hex))[0]))
        return numbers


def write_binary(numbers: list[str], file_location: str):
    steps = len(numbers)
    with open(file_location, mode="wb") as file:
        for step in range(steps):
            file.write(struct.pack('!d', float(numbers[step])))


def convert_dataset(source_location: str, target_location: str, delimiter, per_line: int):
    numbers = read_numbers(source_location, delimiter)
    write_numbers(numbers, target_location, per_line)


def convert_binary_to_csv(source_location: str, target_location: str, per_line: int):
    numbers = read_binary(source_location)
    write_numbers(numbers, target_location, per_line)


def convert_csv_to_binary(source_location: str, target_location: str, delimiter):
    numbers = read_numbers(source_location, delimiter)
    write_binary(numbers, target_location)


def create_file_location(file_location: str):
    return "./Datasets/" + file_location + "/" + file_location


# assumes the base directory of the dataset as the input
def base_buff(file_location):
    fl = create_file_location(file_location)
    numbers = read_numbers(fl, ",")
    write_numbers(numbers, fl + ".csv", 1)
    write_binary(numbers, fl + ".double")


def base_csv(file_location):
    fl = create_file_location(file_location)
    numbers = read_numbers(fl + ".csv", None)
    write_numbers(numbers, fl, 1000)
    write_binary(numbers, fl + ".double")


def base_binary(file_location):
    fl = create_file_location(file_location)
    numbers = read_binary(fl + ".double")
    write_numbers(numbers, fl + ".csv", 1)
    write_numbers(numbers, fl, 1000)


def create_other_datasets(file_location, base):
    match base:
        case "buff":
            base_buff(file_location)
        case "csv":
            base_csv(file_location)
        case "bin":
            base_binary(file_location)
        case _:
            print("unknown base form")


# file = './Datasets/BUFF-dataset/BUFF-dataset.csv'
# file2 = './Datasets/DICTIONARY_8/DICTIONARY_8'
# convert_dataset(file, file + '.csv', ',', 1)
# convert_csv_to_binary(file, file.removesuffix('.csv') + 'bin', None)
