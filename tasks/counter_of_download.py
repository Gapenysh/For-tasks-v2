import os

counter_file = "counter.txt"


def read_file_counter():
    if os.path.exists(counter_file):
        with open(counter_file, "r") as file:
            return int(file.read().strip())
    return 0


def write_file_counter(value):
    with open(counter_file, "w") as file:
        file.write(str(value))
