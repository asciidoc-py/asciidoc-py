"""asciidoc module"""

import sys
from .__metadata__ import VERSION, __version__

__all__ = ['VERSION', '__version__']

# If running as a script, we avoid these imports to avoid a circular
# RuntimeWarning, which is fine as we don't use them in that case.
if "-m" not in sys.argv:
    from .api import AsciiDocAPI
    from .asciidoc import execute, cli
    __all__ += ['AsciiDocAPI', 'execute', 'cli']
