from enum import Enum


class FileSizeUnit(Enum):
    B = 0
    KB = 1
    MB = 2
    GB = 3
    TB = 4


def file_size_convert_to(file_size_bytes: int, convert_to_unit: FileSizeUnit) -> float:
    base: int = 1024
    exponent: int = convert_to_unit.value
    return file_size_bytes / pow(base, exponent)
