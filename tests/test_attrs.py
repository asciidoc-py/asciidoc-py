from asciidoc import attrs
import pytest


testcases = {
    # these test cases fail under future mode
    "pure_legacy": (
        # In future mode, all values are always strings
        (
            'height=100,caption="",link="images/octocat.png"',
            {
                '0': 'height=100,caption="",link="images/octocat.png"',
                'height': 100,
                'caption': '',
                'link': 'images/octocat.png',
            },
        ),
        (
            "height=100,caption='',link='images/octocat.png'",
            {
                '0': "height=100,caption='',link='images/octocat.png'",
                'height': 100,
                'caption': '',
                'link': 'images/octocat.png',
            },
        ),
    ),
    # these test cases pass under both legacy and future modes
    "legacy": (
        # docstring tests
        ('', {}),
        ('hello,world', {'0': 'hello,world', '1': 'hello', '2': 'world'}),
        (
            '"hello", planet="earth"',
            {'0': '"hello", planet="earth"', '1': 'hello', 'planet': 'earth'}
        ),
        # tests taken from
        # https://github.com/asciidoctor/asciidoctor/blob/main/test/attribute_list_test.rb
        ('quote', {'0': 'quote', '1': 'quote'}),
        ('"quote"', {'0': '"quote"', '1': 'quote'}),
        ('""', {'0': '""', '1': ''}),
        ("'quote'", {'0': "'quote'", '1': 'quote'}),
        ("''", {'0': "''", '1': ''}),
        ('\'', {'0': '\'', '1': '\''}),
        ('\'ba\\\'zaar\'', {'0': '\'ba\\\'zaar\'', '1': 'ba\'zaar'}),
        (
            'first, second one, third',
            {
                '0': 'first, second one, third',
                '1': 'first',
                '2': 'second one', '3': 'third',
            },
        ),
        ('=foo=', {'0': '=foo=', '1': '=foo='}),
        ('foo="bar"', {'0': 'foo="bar"', 'foo': 'bar'}),

        ('foo=\'bar\'', {'0': 'foo=\'bar\'', 'foo': 'bar'}),

    ),
    # these tests only pass under future mode
    # tests taken from
    # https://github.com/asciidoctor/asciidoctor/blob/main/test/attribute_list_test.rb
    "future": (
        ('"ba\"zaar"', {'0': '"ba\"zaar"', '1': 'ba"zaar'}),
        ('name=\'', {'0': 'name=\'', 'name': '\''}),
        ('name=\'{val}', {'0': 'name=\'{val}', 'name': '\'{val}'}),
        ('quote , ', {'0': 'quote , ', '1': 'quote', '2': None}),
        (', John Smith', {'0': ', John Smith', '1': None, '2': 'John Smith'}),
        (
            'first,,third,',
            {'0': 'first,,third,', '1': 'first', '2': None, '3': 'third', '4': None}
        ),
        ('foo=bar', {'0': 'foo=bar', 'foo': 'bar'}),
        ('foo=', {'0': 'foo=', 'foo': ''}),
        ('foo=,bar=baz', {'0': 'foo=,bar=baz', 'foo': '', 'bar': 'baz'}),
        (
            'height=100,caption="",link="images/octocat.png"',
            {
                '0': 'height=100,caption="",link="images/octocat.png"',
                'height': '100',
                'caption': '',
                'link': 'images/octocat.png',
            },
        ),
        (
            "height=100,caption='',link='images/octocat.png'",
            {
                '0': "height=100,caption='',link='images/octocat.png'",
                'height': '100',
                'caption': '',
                'link': 'images/octocat.png',
            },
        ),
        (
            'first=value, second=two, third=3',
            {
                '0': 'first=value, second=two, third=3',
                'first': 'value',
                'second': 'two',
                'third': '3',
            },
        ),
        (
            'first=\'value\', second="value two", third=three',
            {
                '0': 'first=\'value\', second="value two", third=three',
                'first': 'value',
                'second': 'value two',
                'third': 'three',
            },
        ),
        (
            "     first    =     'value', second     =\"value two\"     , third=       three      ",  # noqa: E501
            {
                '0': "     first    =     'value', second     =\"value two\"     , third=       three      ",  # noqa: E501
                'first': 'value',
                'second': 'value two',
                'third': 'three',
            },
        ),
        (
            'first, second="value two", third=three, Sherlock Holmes',
            {
                '0': 'first, second="value two", third=three, Sherlock Holmes',
                '1': 'first',
                'second': 'value two',
                'third': 'three',
                '4': 'Sherlock Holmes',
            },
        ),
        (
            'first,,third=,,fifth=five',
            {
                '0': 'first,,third=,,fifth=five',
                '1': 'first',
                '2': None,
                'third': '',
                '4': None,
                'fifth': 'five',
            },
        ),
    )
}


@pytest.mark.parametrize(
    "input,expected",
    testcases["legacy"] + testcases["pure_legacy"],
)
def test_parse_attributes(input, expected):
    output = dict()
    attrs.parse_attributes(input, output)
    assert output == expected


@pytest.mark.parametrize(
    "input,expected",
    testcases['legacy'] + testcases["future"],
)
def test_parse_future_attributes(enable_future_compat, input, expected):
    output = dict()
    attrs.parse_attributes(input, output)
    assert output == expected
