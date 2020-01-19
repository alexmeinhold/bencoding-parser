import pytest

from encoding import (
    encode_integer,
    encode_bytes,
    encode_list,
    encode_dict,
)


def test_integer():
    assert encode_integer(0) == b"i0e"
    assert encode_integer(42) == b"i42e"
    assert encode_integer(-42) == b"i-42e"


def test_bytes():
    assert encode_bytes(b"") == b"0:"
    assert encode_bytes(b"spam") == b"4:spam"


def test_list():
    assert encode_list([]) == b"le"
    assert encode_list([b"spam", 42]) == b"l4:spami42ee"


def test_dict():
    assert encode_dict({}) == b"de"
    assert encode_dict({b"bar": b"spam", b"foo": 42}) == b"d3:bar4:spam3:fooi42ee"

    data = {
        b"test": [b"hello", 5, {b"a": 1}],
        b"longlist": [[b"a", b"b", b"c"], [1, 2, [3, 4, 5]]],
    }

    assert (
        encode_dict(data)
        == b"d8:longlistll1:a1:b1:celi1ei2eli3ei4ei5eeee4:testl5:helloi5ed1:ai1eeee"
    )
