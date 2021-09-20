import pytest
from asciidoc import utils


@pytest.mark.parametrize(
    "input,expected",
    [
        (' a ', 'a'),
        ('"a"', 'a'),
        ('  "b ', '"b'),
        ('  b" ', 'b"'),
        ('""', '""'),
    ],
)
def test_strip_quotes(input, expected):
    assert utils.strip_quotes(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('a', 'b')),
        (('a', 'b', ''), ('a', 'b', '')),
        (('', 'a', 'b', ''), ('a', 'b', '')),
    ],
)
def test_lstrip_list(input, expected):
    assert utils.lstrip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('', 'a', 'b')),
        (('a', 'b', ''), ('a', 'b')),
        (('', 'a', 'b', ''), ('', 'a', 'b')),
    ],
)
def test_rstrip_list(input, expected):
    assert utils.rstrip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('a', 'b')),
        (('a', 'b', ''), ('a', 'b')),
        (('', 'a', 'b', ''), ('a', 'b')),
    ],
)
def test_strip_list(input, expected):
    assert utils.strip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ((1,), True),
        ([1], True),
        ('a', False),
    ],
)
def test_is_array(input, expected):
    assert utils.is_array(input) == expected


@pytest.mark.parametrize(
    "n,d,expected",
    [
        (42.0, 0, 42),
        (42.4, 0, 42),
        (42.5, 0, 43),
        (42.6, 0, 43),
        (42.9, 0, 43),
        (42.0, 2, 42),
        (42.5, 2, 42.5),
        (42.550, 2, 42.55),
        (42.554, 2, 42.55),
        (42.555, 2, 42.56),
        (42.556, 2, 42.56),
        (42.559, 2, 42.56),
    ],
)
def test_py2round(n, d, expected):
    assert utils.py2round(n, d) == expected
