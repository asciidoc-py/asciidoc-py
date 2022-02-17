

from asciidoc.message import Message
from asciidoc.plugin import Plugin

from .utils import Struct, TEST_DIR

PLUGIN_DIR = TEST_DIR / 'plugin'
CONFIG = Struct(get_load_dirs=lambda: [str(PLUGIN_DIR)], verbose=True)


def test_plugin_list(capsys) -> None:
    plugin = Plugin('backend', Message(None, None, CONFIG, None), CONFIG)
    plugin.list([])
    captured = capsys.readouterr()
    backend_dir = PLUGIN_DIR / 'backends'
    assert captured.out == "{}\n{}\n".format(backend_dir / 'bar', backend_dir / 'foo')
    assert captured.err == ''
