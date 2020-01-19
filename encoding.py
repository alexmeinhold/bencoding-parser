def encode_integer(integer: int) -> bytes:
    return f"i{str(integer)}e".encode()


def encode_bytes(byte_string: bytes) -> bytes:
    return str(len(byte_string)).encode() + b":" + byte_string


def encode_list(l: list) -> bytes:
    encoded_list = b"l"
    for value in l:
        encoded_list += encode_value(value)
    return encoded_list + b"e"


def encode_dict(d: dict) -> bytes:
    encoded_dict = b"d"
    sorted_dict = sorted(d.items(), key=lambda x: x[0])

    for (key, value) in sorted_dict:
        encoded_dict += encode_bytes(key)
        encoded_dict += encode_value(value)

    return encoded_dict + b"e"


def encode_value(value) -> bytes:
    encoded_value = b""
    value_type = type(value)

    if value_type == int:
        encoded_value = encode_integer(value)
    elif value_type == bytes:
        encoded_value = encode_bytes(value)
    elif value_type == list:
        encoded_value = encode_list(value)
    elif value_type == dict:
        encoded_value = encode_dict(value)

    return encoded_value
