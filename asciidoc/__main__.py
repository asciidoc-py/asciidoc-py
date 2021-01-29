try:
    from .asciidoc import cli, set_caller
except ImportError:
    from asciidoc import cli, set_caller

set_caller(__name__)
cli()
