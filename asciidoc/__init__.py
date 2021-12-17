"""asciidoc module"""

from .api import AsciiDocAPI
from .asciidoc import execute, cli
from .__metadata__ import VERSION, __version__

__all__ = ['AsciiDocAPI', 'execute', 'cli', 'VERSION', '__version__']
