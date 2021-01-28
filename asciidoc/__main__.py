try:
    from .asciidoc import cli
except ImportError:
    from asciidoc import cli

cli()
