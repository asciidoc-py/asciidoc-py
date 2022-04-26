import pytest
from pytest_mock import MockerFixture
from typing import Optional, Tuple

from asciidoc import utils


@pytest.mark.parametrize(
    "input,expected",
    (
        ('/home/user', '/home/user'),
        ('~', None),
    )
)
def test_userdir(mocker: MockerFixture, input: str, expected: Optional[str]) -> None:
    mocker.patch('os.path.expanduser', return_value=input)
    assert utils.userdir() == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        (' a ', 'a'),
        ('"a"', 'a'),
        ('  "b ', '"b'),
        ('  b" ', 'b"'),
        ('""', '""'),
    ),
)
def test_strip_quotes(input: str, expected: str) -> None:
    assert utils.strip_quotes(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('a', 'b')),
        (('a', 'b', ''), ('a', 'b', '')),
        (('', 'a', 'b', ''), ('a', 'b', '')),
    ),
)
def test_lstrip_list(input: Tuple[str, ...], expected: Tuple[str, ...]) -> None:
    assert utils.lstrip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('', 'a', 'b')),
        (('a', 'b', ''), ('a', 'b')),
        (('', 'a', 'b', ''), ('', 'a', 'b')),
    ),
)
def test_rstrip_list(input: Tuple[str, ...], expected: Tuple[str, ...]) -> None:
    assert utils.rstrip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        (('a', 'b'), ('a', 'b')),
        (('', 'a', 'b'), ('a', 'b')),
        (('a', 'b', ''), ('a', 'b')),
        (('', 'a', 'b', ''), ('a', 'b')),
    ),
)
def test_strip_list(input: Tuple[str, ...], expected: Tuple[str, ...]) -> None:
    assert utils.strip_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ((1,), True),
        ([1], True),
        ('a', False),
    ),
)
def test_is_array(input, expected):
    assert utils.is_array(input) == expected


@pytest.mark.parametrize(
    "n,d,expected",
    (
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
    ),
)
def test_py2round(n: float, d: int, expected: float) -> None:
    assert utils.py2round(n, d) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ('"hello","world"', {'1': 'hello', '2': 'world'}),
        ('"hello", planet="earth"', {'1': 'hello'}),
    )
)
def test_get_args(input, expected):
    assert utils.get_args(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ('"hello", "world"', {}),
        ('planet="earth"', {'planet': 'earth'}),
        ('"hello",planet="earth"', {'planet': 'earth'}),
        ('planet="earth",foo="bar"', {'planet': 'earth', 'foo': 'bar'}),
    )
)
def test_get_kwargs(input, expected):
    assert utils.get_kwargs(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ('1,2,3', [1, 2, 3]),
        ('"a", "b", "c"', ['a', 'b', 'c'])
    )
)
def test_parse_to_list(input, expected):
    assert utils.parse_to_list(input) == expected
