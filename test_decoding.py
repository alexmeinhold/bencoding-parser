import pytest

from decoding import (
    decode_integer,
    decode_bytes,
    decode_list,
    decode_dict,
)


def test_integer():
    assert decode_integer(b"i10e") == (10, b"")
    assert decode_integer(b"i10e4:abcd") == (10, b"4:abcd")

    with pytest.raises(ValueError):
        decode_integer(b"i-0e")


def test_bytes():
    assert decode_bytes(b"0:") == (b"", b"")
    assert decode_bytes(b"4:spam") == (b"spam", b"")


def test_list():
    assert decode_list(b"le") == ([], b"")
    assert decode_list(b"l4:spami42ee") == ([b"spam", 42], b"")


def test_dict():
    assert decode_dict(b"de") == ({}, b"")
    assert decode_dict(b"d3:bar4:spam3:fooi42ee") == (
        {b"bar": b"spam", b"foo": 42},
        b"",
    )

    assert decode_dict(b"d3:barlee") == ({b"bar": []}, b"")
    assert decode_dict(b"d3:barde4:abcdlleee") == ({b"bar": {}, b"abcd": [[]]}, b"")
    assert decode_dict(b"d1:ali1ei2eli1ei2eld1:aleeeee1:bdee") == (
        {b"a": [1, 2, [1, 2, [{b"a": []}]]], b"b": {}},
        b"",
    )
