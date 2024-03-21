import struct
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


def create_other_dataset(fl, base, target):
    match base:
        case "bin":
            numbers = read_binary(fl + ".double")
            if target == "buff":
                write_numbers(numbers, fl + "", 1000)
            elif target == "csv":
                write_numbers(numbers, fl + ".csv", 1)
        case "csv":
            numbers = read_numbers(fl + ".csv", None)
            if target == "buff":
                write_numbers(numbers, fl + "", 1000)
            elif target == "bin":
                write_binary(numbers, fl + ".double")
        case "buff":
            numbers = read_numbers(fl, ",")
            if target == "csv":
                write_numbers(numbers, fl + ".csv", 1)
            elif target == "bin":
                write_binary(numbers, fl + ".double")
        case _:
            print("unknown base form")
