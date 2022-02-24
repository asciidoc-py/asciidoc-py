from asciidoc import attrs
import pytest

@pytest.mark.parametrize(
    "input,expected",
    (
        # docstring tests
        ('', {}),
        ('hello,world', {'0': 'hello,world', '1': 'hello', '2': 'world'}),
        ('"hello", planet="earth"', {'0': '"hello", planet="earth"', '1': 'hello', 'planet': 'earth'}),
        # tests taken from https://github.com/asciidoctor/asciidoctor/blob/main/test/attribute_list_test.rb
        # commented out tests are currently supported by asciidoc.py
        ('quote', {'0': 'quote', '1': 'quote'}),
        ('"quote"', {'0': '"quote"', '1': 'quote'}),
        ('""', {'0': '""', '1': ''}),
        # ('"ba\"zaar"', {'0': '"ba\"zaar"', '1': 'ba"zaar'}),
        ("'quote'", {'0': "'quote'", '1': 'quote'}),
        ("''", {'0': "''", '1': ''}),
        ('\'', {'0': '\'', '1': '\''}),
        #('name=\'', {'0': 'name=\'', 'name': '\''}),
        #('name=\'{val}', {'0': 'name=\'{val}', 'name': '\'{val}'}),
        ('\'ba\\\'zaar\'', {'0': '\'ba\\\'zaar\'', '1': 'ba\'zaar'}),
        #('quote , ', {'0': 'quote , ', '1': 'quote', '2': None}),
        #(', John Smith', {'0': ', John Smith', '1': None, '2': 'John Smith'}),
        ('first, second one, third', {'0': 'first, second one, third', '1': 'first', '2': 'second one', '3': 'third'}),
        #('first,,third,', {'0': 'first,,third,', '1': 'first', '2': None, '3': 'third', '4': None}),
        ('=foo=', {'0': '=foo=', '1': '=foo='}),
        #('foo=bar', {'0': 'foo=bar', 'foo': 'bar'}),
        ('foo="bar"', {'0': 'foo="bar"', 'foo': 'bar'}),
        ('height=100,caption="",link="images/octocat.png"', {'0': 'height=100,caption="",link="images/octocat.png"', 'height': 100, 'caption': '', 'link': 'images/octocat.png'}),
        ('foo=\'bar\'', {'0': 'foo=\'bar\'', 'foo': 'bar'}),
        ("height=100,caption='',link='images/octocat.png'", {'0': "height=100,caption='',link='images/octocat.png'", 'height': 100, 'caption': '', 'link': 'images/octocat.png'}),
        #('foo=', {'0': 'foo=', 'foo': ''}),
        #('foo=,bar=baz', {'0': 'foo=,bar=baz', 'foo': '', 'bar': 'baz'}),
        #('first=value, second=two, third=3', {0: 'first=value, second=two, third=3', 'first': 'value', 'second': 'two', 'third': '3'}),
        #('first=\'value\', second="value two", third=three', {0: 'first=\'value\', second="value two", third=three', 'first': 'value', 'second': 'value two', 'third': 'three'}),
        #("     first    =     'value', second     =\"value two\"     , third=       three      ", {'0': "     first    =     'value', second     =\"value two\"     , third=       three      ", 'first': 'value', 'second': 'value two', 'third': 'three'}),
        #('first, second="value two", third=three, Sherlock Holmes', {'0': 'first, second="value two", third=three, Sherlock Holmes', '1': 'first', 'second': 'value two', 'third': 'three', '4': 'Sherlock Holmes'}),
        #('first,,third=,,fifth=five', {0: 'first,,third=,,fifth=five', '1': 'first', '2': None, 'third': '', '4': None, 'fifth': 'five'}),
    )
)
def test_parse_attributes(input, expected):
    output = dict()
    attrs.parse_attributes(input, output)
    assert output == expected
