class EAsciiDoc(Exception):
    """Exceptions raised by the main asciidoc process"""
    pass


class AsciiDocError(Exception):
    """Exceptions raised by the asciidoc API"""
    pass

class OnlyBookLvl0Sections(AsciiDocError):
    """ if a level 0 section is discovered and the doctype is not book
    """
    pass
