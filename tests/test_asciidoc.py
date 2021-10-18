from asciidoc import asciidoc
import io
import pytest


@pytest.mark.parametrize(
    "input,expected",
    (
        (
            '{attach}file.txt',
            '<div class="paragraph"><p></p></div>\r\n'
        ),
        (
            '\\{attach}file{0}.txt',
            '<div class="paragraph"><p></p></div>\r\n'
        ),
        (
            '\\{attach}file.txt',
            '<div class="paragraph"><p>{attach}file.txt</p></div>\r\n'
        ),
        (
            '\\{0}file.txt',
            '<div class="paragraph"><p>{0}file.txt</p></div>\r\n'
        ),
        (
            'link:{attach}file.txt[file]',
            '<div class="paragraph"><p></p></div>\r\n'
        ),
        (
            'link:\\{attach}file.txt[file]',
            '<div class="paragraph"><p>' +
            '<a href="{attach}file.txt">file</a></p></div>\r\n'
        ),
        (
            'link:\\{attach}file\\{0}.txt[file\\{bar}too\\{1}]',
            '<div class="paragraph"><p><a href="{attach}file{0}.txt">' +
            'file{bar}too{1}</a></p></div>\r\n'
        ),
        (
            'image:\\{attach}file.jpg[]',
            '<div class="paragraph"><p><span class="image">\r\n' +
            '<img src="{attach}file.jpg" alt="{attach}file.jpg" />\r\n' +
            '</span></p></div>\r\n'
        ),
        (
            'image:\\{attach}file.jpg[foo]',
            '<div class="paragraph"><p><span class="image">\r\n' +
            '<img src="{attach}file.jpg" alt="foo" />\r\n</span></p></div>\r\n'
        ),
        (
            'image:\\{attach}file.jpg[\\{bar}?]',
            '<div class="paragraph"><p><span class="image">\r\n' +
            '<img src="{attach}file.jpg" alt="{bar}?" />\r\n</span></p></div>\r\n'
        ),
    )
)
def test_ignore_attribute(input, expected):
    infile = io.StringIO(input)
    outfile = io.StringIO()
    options = [
        ('--out-file', outfile),
        ('--no-header-footer', '')
    ]
    asciidoc.execute('asciidoc', options, [infile])
    assert outfile.getvalue() == expected
