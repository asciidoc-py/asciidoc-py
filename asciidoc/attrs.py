import re
import typing

from .utils import get_args, get_kwargs


def parse_attributes(attrs: str, output_dict: typing.Dict) -> None:
    """Update a dictionary with name/value attributes from the attrs string.
    The attrs string is a comma separated list of values and keyword name=value
    pairs. Values must precede keywords and are named '1','2'... The entire
    attributes list is named '0'. If keywords are specified string values must
    be quoted. Examples:

    attrs: ''
    output_dict: {}

    attrs: 'hello,world'
    output_dict: {'2': 'world', '0': 'hello,world', '1': 'hello'}

    attrs: '"hello", planet="earth"'
    output_dict: {'planet': 'earth', '0': '"hello", planet="earth"', '1': 'hello'}
    """
    if not attrs:
        return
    output_dict['0'] = attrs
    # Replace line separators with spaces so line spanning works.
    s = re.sub(r'\s', ' ', attrs)
    d = {}
    try:
        d.update(get_args(s))
        d.update(get_kwargs(s))
        for v in list(d.values()):
            if not (isinstance(v, str)
                    or isinstance(v, int) or isinstance(v, float) or v is None):
                raise Exception
    except Exception:
        s = s.replace('"', '\\"')
        s = s.split(',')
        s = ['"' + x.strip() + '"' for x in s]
        s = ','.join(s)
        try:
            d = {}
            d.update(get_args(s))
            d.update(get_kwargs(s))
        except Exception:
            return  # If there's a syntax error leave with {0}=attrs.
        for k in list(d.keys()):  # Drop any empty positional arguments.
            if d[k] == '':
                del d[k]
    output_dict.update(d)
    assert len(d) > 0
