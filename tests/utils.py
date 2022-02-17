from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent / '__test_data__'


class Struct:
    """
    Use this to make "mock" version of asciidoc classes. Usage is passing in kwargs,
    and these are set to the properties of the class.

    >>> a = Struct(foo=1, bar=2)
    >>> a.foo
    1
    >>> a.bar
    2
    """
    def __init__(self, **entries): self.__dict__.update(entries)
