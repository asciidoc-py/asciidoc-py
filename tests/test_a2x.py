from asciidoc import a2x
import io
import pytest


@pytest.mark.parametrize(
    "input,expected",
    (
        (
            ['a2x', '-vv', '-L', "--asciidoc-opts=-f ../build/mscgen-filter.conf -f ../build/diag-filter.conf -f ../build/docinfo-releaseinfo.conf -a srcdir='/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests' -a commondir='../common'", '--dblatex-opts=-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', '-a', 'docinfo', '-a', 'revnumber=DRAFT ', '-a', 'revdate=unknown', 'test-usermanual.adoc'],
            (
                ['-vv', '-L', "--asciidoc-opts=-f ../build/mscgen-filter.conf -f ../build/diag-filter.conf -f ../build/docinfo-releaseinfo.conf -a srcdir='/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests' -a commondir='../common'", '--dblatex-opts=-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', '-a', 'docinfo', '-a', 'revnumber=DRAFT ', '-a', 'revdate=unknown', 'test-usermanual.adoc'],
                {'attributes': ['docinfo', 'revnumber=DRAFT ', 'revdate=unknown'], 'asciidoc_opts': ['-f', '../build/mscgen-filter.conf', '-f', '../build/diag-filter.conf', '-f', '../build/docinfo-releaseinfo.conf', '-a', 'srcdir=/home/user/code/osmo-dev/src/osmo-gsm-manuals/tests', '-a', 'commondir=../common'], 'copy': False, 'conf_file': None, 'destination_dir': None, 'doctype': None, 'backend': None, 'epubcheck': False, 'format': 'pdf', 'icons': False, 'icons_dir': None, 'keep_artifacts': False, 'lynx': False, 'no_xmllint': True, 'dry_run': False, 'resources': [], 'resource_manifest': None, 'skip_asciidoc': False, 'stylesheet': None, 'safe': False, 'dblatex_opts': '-s ../build/custom-dblatex.sty -P draft.mode=yes -P draft.watermark=0', 'backend_opts': '', 'fop': False, 'fop_opts': '', 'xsltproc_opts': '', 'xsl_file': None, 'verbose': 2},
                ['test-usermanual.adoc'],
            ),
        ),
        (
            ['a2x', '-v', "--asciidoc-opts=-v -f doc/asciidoc.conf -a manmanual='Pakku Manual' -a mansource='Pakku' -a manversion=0.14-36g22678d2", 'doc/pakku.conf.5.txt'],
            (
                ['-v', "--asciidoc-opts=-v -f doc/asciidoc.conf -a manmanual='Pakku Manual' -a mansource='Pakku' -a manversion=0.14-36g22678d2", 'doc/pakku.conf.5.txt'],
                {'attributes': [], 'asciidoc_opts': ['-v', '-f', 'doc/asciidoc.conf', '-a', 'manmanual=Pakku Manual', '-a', 'mansource=Pakku', '-a', 'manversion=0.14-36g22678d2'], 'copy': False, 'conf_file': None, 'destination_dir': None, 'doctype': None, 'backend': None, 'epubcheck': False, 'format': 'pdf', 'icons': False, 'icons_dir': None, 'keep_artifacts': False, 'lynx': False, 'no_xmllint': False, 'dry_run': False, 'resources': [], 'resource_manifest': None, 'skip_asciidoc': False, 'stylesheet': None, 'safe': False, 'dblatex_opts': '', 'backend_opts': '', 'fop': False, 'fop_opts': '', 'xsltproc_opts': '', 'xsl_file': None, 'verbose': 1},
                ['doc/pakku.conf.5.txt'],
            ),
        ),
    )
)
def test_parse_args(input, expected):
    argv, opts, args = a2x.parse_args(input)
    assert argv == expected[0]
    assert opts == expected[1]
    assert args == expected[2]
