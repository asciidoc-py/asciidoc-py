from asciidoc.blocks import table
import pytest


@pytest.mark.parametrize(
    "input,expected",
    (
        (None, (None, None)),
        ('', (None, None)),
        ('<', ('left', None)),
        ('^', ('center', None)),
        ('>', ('right', None)),
        ('.<', (None, 'top')),
        ('.^', (None, 'middle')),
        ('.>', (None, 'bottom')),
        ('<.<', ('left', 'top')),
        ('^.<', ('center', 'top')),
        ('>.<', ('right', 'top')),
        ('<.^', ('left', 'middle')),
        ('^.^', ('center', 'middle')),
        ('>.^', ('right', 'middle')),
        ('<.>', ('left', 'bottom')),
        ('^.>', ('center', 'bottom')),
        ('>.>', ('right', 'bottom')),
    )
)
def test_parse_align_spec(input, expected):
    assert table.parse_align_spec(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        (None, (1, 1)),
        ('', (1, 1)),
        ('0', (1, 1)),
        ('.0', (1, 1)),
        ('0.0', (1, 1)),
        ('2', (2, 1)),
        ('.2', (1, 2)),
        ('3.2', (3, 2)),
    )
)
def test_parse_table_span_spec(input, expected):
    assert table.parse_table_span_spec(input) == expected
