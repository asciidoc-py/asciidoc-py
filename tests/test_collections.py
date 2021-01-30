import pytest
from asciidoc.collections import AttrDict, DefaultAttrDict, InsensitiveDict


def test_attr_dict():
    d = AttrDict()
    d.a = 1
    d['b'] = 2
    assert d['a'] == 1
    assert d.b == 2
    del d['a']
    del d.b
    assert 'a' not in d
    assert 'b' not in d
    assert d.c is None

    with pytest.raises(AttributeError):
        del d.c


def test_default_attr_dict():
    d = DefaultAttrDict()
    with pytest.raises(AttributeError):
        d.a
    d._default = 'test'

    assert d.a == 'test'


def test_insensitive_dict():
    d = InsensitiveDict()
    d['A'] = 1
    assert d['a'] == 1
    d['aBaBa'] = 2
    assert 'AbAbA' in d
    del d['abaBA']
    assert ('ababa' in d) is False
