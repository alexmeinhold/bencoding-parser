from typing import Any

import string


END_LIST = [s.encode() for s in ["le", "l", "e", ""]]
END_DICT = [s.encode() for s in ["de", "d", "e", ""]]


def decode_integer(bencoded_int: bytes) -> (int, bytes):
    index = 0

    while bencoded_int[index] != ord("e"):
        index += 1

    number = bencoded_int[1:index]

    if number == b"-0":
        raise ValueError

    return int(number), bencoded_int[index + 1 :]


def decode_bytes(bencoded_bytes: bytes) -> (bytes, bytes):
    index = 0

    while bencoded_bytes[index] != ord(":"):
        index += 1

    length = int(bencoded_bytes[:index])

    return (
        bencoded_bytes[index + 1 : (index + 1) + length],
        bencoded_bytes[(index + 1) + length :],
    )


def decode_list(bencoded_list: bytes) -> (list, bytes):
    if bencoded_list[:2] in END_LIST:
        return [], bencoded_list[2:]

    value, rest = decode_value(bencoded_list[1:])
    decoded_list, rest = decode_list(b"l" + rest)
    return [value] + decoded_list, rest


def decode_dict(bencoded_dict: bytes) -> (dict, bytes):
    if bencoded_dict[:2] in END_DICT:
        return ({}, bencoded_dict[2:])

    key, rest = decode_bytes(bencoded_dict[1:])
    value, rest = decode_value(rest)

    decoded_dict, rest = decode_dict(b"d" + rest)
    return {**{key: value}, **decoded_dict}, rest


def decode_value(bencoded_value: bytes) -> (Any, bytes):
    first_char = bencoded_value[0]

    value = b""
    rest = b""

    if first_char in string.digits.encode():
        value, rest = decode_bytes(bencoded_value)
    elif first_char == ord("i"):
        value, rest = decode_integer(bencoded_value)
    elif first_char == ord("l"):
        value, rest = decode_list(bencoded_value)
    elif first_char == ord("d"):
        value, rest = decode_dict(bencoded_value)

    return value, rest


def decode(bencoded_data: bytes) -> Any:
    return decode_value(bencoded_data)[0]
