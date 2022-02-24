# flake8: noqa E501

from asciidoc import a2x
import pytest


@pytest.mark.parametrize(
    "input,expected_argv,expected_opts,expected_args",
    (
        (
            ['a2x', '--xsltproc-opts', '-param man.endnotes.list.enabled 0 -param man.endnotes.are.numbered 0', '--asciidoc-opts', '-a pacman_date=2020-07-05 -a srcext=.src.tar.gz -a pkgext=.pkg.tar.gz', '../doc/alpm-hooks.5.asciidoc'],
            ['--xsltproc-opts', '-param man.endnotes.list.enabled 0 -param man.endnotes.are.numbered 0', '--asciidoc-opts', '-a pacman_date=2020-07-05 -a srcext=.src.tar.gz -a pkgext=.pkg.tar.gz', '../doc/alpm-hooks.5.asciidoc'],
            {'attributes': [], 'asciidoc_opts': ['-a', 'pacman_date=2020-07-05', '-a', 'srcext=.src.tar.gz', '-a', 'pkgext=.pkg.tar.gz'], 'copy': False, 'conf_file': None, 'destination_dir': None, 'doctype': None, 'backend': None, 'epubcheck': False, 'format': 'pdf', 'icons': False, 'icons_dir': None, 'keep_artifacts': False, 'lynx': False, 'no_xmllint': False, 'dry_run': False, 'resources': [], 'resource_manifest': None, 'skip_asciidoc': False, 'stylesheet': None, 'safe': False, 'dblatex_opts': '', 'backend_opts': '', 'fop': False, 'fop_opts': '', 'xsltproc_opts': '-param man.endnotes.list.enabled 0 -param man.endnotes.are.numbered 0', 'xsl_file': None, 'verbose': 0},
            ['../doc/alpm-hooks.5.asciidoc'],
        ),
        (
            ['a2x', '-vv', '-L', "--asciidoc-opts=-f ../build/mscgen-filter.conf -f ../build/diag-filter.conf -f ../build/docinfo-releaseinfo.conf -a srcdir='/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests' -a commondir='../common'", '--dblatex-opts=-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', '-a', 'docinfo', '-a', 'revnumber=DRAFT ', '-a', 'revdate=unknown', 'test-usermanual.adoc'],
            ['-vv', '-L', "--asciidoc-opts=-f ../build/mscgen-filter.conf -f ../build/diag-filter.conf -f ../build/docinfo-releaseinfo.conf -a srcdir='/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests' -a commondir='../common'", '--dblatex-opts=-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', '-a', 'docinfo', '-a', 'revnumber=DRAFT ', '-a', 'revdate=unknown', 'test-usermanual.adoc'],
            {'attributes': ['docinfo', 'revnumber=DRAFT ', 'revdate=unknown'], 'asciidoc_opts': ['-f', '../build/mscgen-filter.conf', '-f', '../build/diag-filter.conf', '-f', '../build/docinfo-releaseinfo.conf', '-a', 'srcdir=/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests', '-a', 'commondir=../common'], 'copy': False, 'conf_file': None, 'destination_dir': None, 'doctype': None, 'backend': None, 'epubcheck': False, 'format': 'pdf', 'icons': False, 'icons_dir': None, 'keep_artifacts': False, 'lynx': False, 'no_xmllint': True, 'dry_run': False, 'resources': [], 'resource_manifest': None, 'skip_asciidoc': False, 'stylesheet': None, 'safe': False, 'dblatex_opts': '-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', 'backend_opts': '', 'fop': False, 'fop_opts': '', 'xsltproc_opts': '', 'xsl_file': None, 'verbose': 2},
            ['test-usermanual.adoc'],
        ),
        (
            ['a2x', '-v', "--asciidoc-opts=-v -f doc/asciidoc.conf -a manmanual='Pakku Manual' -a mansource='Pakku' -a manversion=0.14-36g22678d2", 'doc/pakku.conf.5.txt'],
            ['-v', "--asciidoc-opts=-v -f doc/asciidoc.conf -a manmanual='Pakku Manual' -a mansource='Pakku' -a manversion=0.14-36g22678d2", 'doc/pakku.conf.5.txt'],
            {'attributes': [], 'asciidoc_opts': ['-v', '-f', 'doc/asciidoc.conf', '-a', 'manmanual=Pakku Manual', '-a', 'mansource=Pakku', '-a', 'manversion=0.14-36g22678d2'], 'copy': False, 'conf_file': None, 'destination_dir': None, 'doctype': None, 'backend': None, 'epubcheck': False, 'format': 'pdf', 'icons': False, 'icons_dir': None, 'keep_artifacts': False, 'lynx': False, 'no_xmllint': False, 'dry_run': False, 'resources': [], 'resource_manifest': None, 'skip_asciidoc': False, 'stylesheet': None, 'safe': False, 'dblatex_opts': '', 'backend_opts': '', 'fop': False, 'fop_opts': '', 'xsltproc_opts': '', 'xsl_file': None, 'verbose': 1},
            ['doc/pakku.conf.5.txt'],
        ),
    )
)
def test_parse_args(input, expected_argv, expected_opts, expected_args):
    argv, opts, args = a2x.parse_args(input)
    assert argv == expected_argv
    assert opts == expected_opts
    assert args == expected_args


@pytest.mark.parametrize(
    "input,expected",
    (
        (b'', 'utf-8'),
        (b'<?xml version="1.0" encoding="ASCII"?>', 'ASCII'),
        (b'<?xml version="1.0"?>', 'utf-8'),
        (
            b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=ASCII">',
            'ASCII',
        ),
        (
            b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n<head>\n<title>Foo</title>\n</head>',
            'utf-8',
        ),
    ),
)
def test_get_encoding(input, expected):
    assert a2x.get_encoding(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    (
        ('', []),
        (
            """
// a2x: --foo --bar
//      a2x: --baz
// a2x: "--foo --bar
// a2x: --baz" --qux
            """,
            ['--foo', '--bar', '--baz', "--foo --bar --baz", '--qux'],
        ),
    )
)
def test_get_source_options(tmp_path, input, expected):
    test_file = tmp_path / 'test_file.adoc'
    test_file.write_text(input)
    assert a2x.get_source_options(str(test_file)) == expected


def test_get_source_options_non_existing_file():
    assert a2x.get_source_options('/some/non/existing/file') == []
