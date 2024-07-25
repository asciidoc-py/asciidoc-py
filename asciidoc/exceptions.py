class EAsciiDoc(Exception):
    """Exceptions raised by the main asciidoc process"""
    pass


class EOnlyBookLvl0Sections(EAsciiDoc):
    """ Parser only allows lvl 0 headings on doctype book
    """
    pass


class AsciiDocError(Exception):
    """Exceptions raised by the asciidoc API"""
    pass
