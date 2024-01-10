import csv
from math import ceil


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


def convert_textfiles(source_location: str, target_location: str, delimiter, per_line: int):
    numbers = read_numbers(source_location, delimiter)
    write_numbers(numbers, target_location, per_line)


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


file = './Datasets/BUFF-dataset/BUFF-dataset'
#file = './Datasets/t502861995_c0/t502861995_c0.csv'
convert_textfiles(file, file + '.csv', ',', 1)
