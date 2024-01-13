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


def one_to_two(file_location):
    with open(file_location, newline='') as csvfile:
        string_with_breaks = csvfile.read()
        target_file_lines = string_with_breaks.count('\n')/1000 + 1
        string_with_commas = {}
        for x in range(target_file_lines):
            for y in range(1000):
                string_with_commas[x] = string_with_breaks.replace('\n', ',')
        with open(file_location.removesuffix('.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(string_with_commas)


def two_to_one(file_location):
    with open(file_location, newline='') as file:
        reader = csv.reader(file)
        with open(file_location + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in reader:
                for i in range(len(row)):
                    writer.writerow([row[i]])


file = './Datasets/t502861995_c0/t502861995_c0.csv'
file2 = './Datasets/Btr_double1/DICTIONARY_8.double'
# convert_dataset(file, file + '.csv', ',', 1)
convert_csv_to_binary(file, file.removesuffix('.csv') + 'bin', None)
