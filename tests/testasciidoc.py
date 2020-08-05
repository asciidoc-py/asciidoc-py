#!/usr/bin/env python3

__version__ = '0.3.0'


import difflib
import io
import os
from pathlib import Path
import re
import shutil
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
import asciidocapi  # noqa: E402

# Default backends.
BACKENDS = ('html4', 'xhtml11', 'docbook', 'docbook5', 'html5')
BACKEND_EXT = {
    'html4': '.html',
    'xhtml11': '.html',
    'docbook': '.xml',
    'docbook5': '.xml',
    'slidy': '.html',
    'html5': '.html'
}


def iif(condition, iftrue, iffalse=None):
    """
    Immediate if c.f. ternary ?: operator.
    False value defaults to '' if the true value is a string.
    False value defaults to 0 if the true value is a number.
    """
    if iffalse is None:
        if isinstance(iftrue, str):
            iffalse = ''
        if type(iftrue) in (int, float):
            iffalse = 0
    if condition:
        return iftrue
    else:
        return iffalse


def message(msg=''):
    print(msg, file=sys.stderr)


def strip_end(lines):
    """
    Strip blank strings from the end of list of strings.
    """
    for i in range(len(lines) - 1, -1, -1):
        if not lines[i]:
            del lines[i]
        else:
            break


def normalize_data(lines):
    """
    Strip comments and trailing blank strings from lines.
    """
    result = [s for s in lines if not s.startswith('#')]
    strip_end(result)
    return result


class AsciiDocTest(object):
    def __init__(self):
        self.number = None      # Test number (1..).
        self.name = ''          # Optional test name.
        self.title = ''         # Optional test name.
        self.description = []   # List of lines followoing title.
        self.source = None      # AsciiDoc test source file name.
        self.options = []
        self.attributes = {'asciidoc-version': 'test'}
        self.backends = BACKENDS
        self.requires = []      # list of dependencies to check for for the test
        self.confdir = None
        self.datadir = None     # Where output files are stored.
        self.disabled = False
        self.passed = self.skipped = self.failed = 0

    def backend_filename(self, backend):
        """
        Return the path name of the backend  output file that is generated from
        the test name and output file type.
        """
        return '%s-%s%s' % (
                os.path.normpath(os.path.join(self.datadir, self.name)),
                backend,
                BACKEND_EXT[backend])

    def parse(self, lines, confdir, datadir):
        """
        Parse conf file test section from list of text lines.
        """
        self.__init__()
        self.confdir = confdir
        self.datadir = datadir
        lines = Lines(lines)
        while not lines.eol():
            text = lines.read_until(r'^%')
            if text:
                if not text[0].startswith('%'):
                    if text[0][0] == '!':
                        self.disabled = True
                        self.title = text[0][1:]
                    else:
                        self.title = text[0]
                    self.description = text[1:]
                    continue
                reo = re.match(r'^%\s*(?P<directive>[\w_-]+)', text[0])
                if not reo:
                    raise ValueError
                directive = reo.groupdict()['directive']
                data = normalize_data(text[1:])
                if directive == 'source':
                    if data:
                        self.source = os.path.normpath(os.path.join(
                                self.confdir, os.path.normpath(data[0])))
                elif directive == 'options':
                    self.options = eval(' '.join(data))
                    for i, v in enumerate(self.options):
                        if isinstance(v, str):
                            self.options[i] = (v, None)
                elif directive == 'attributes':
                    self.attributes.update(eval(' '.join(data)))
                elif directive == 'backends':
                    self.backends = eval(' '.join(data))
                elif directive == 'name':
                    self.name = data[0].strip()
                elif directive == 'requires':
                    self.requires = eval(' '.join(data))
                else:
                    raise ValueError
        if not self.title:
            self.title = self.source
        if not self.name:
            self.name = os.path.basename(os.path.splitext(self.source)[0])

    def is_missing(self, backend):
        """
        Returns True if there is no output test data file for backend.
        """
        return not os.path.isfile(self.backend_filename(backend))

    def is_missing_or_outdated(self, backend):
        """
        Returns True if the output test data file is missing or out of date.
        """
        return self.is_missing(backend) or (
               os.path.getmtime(self.source)
               > os.path.getmtime(self.backend_filename(backend)))

    def get_expected(self, backend):
        """
        Return expected test data output for backend.
        """
        with open(self.backend_filename(backend), encoding='utf-8') as open_file:
            result = open_file.readlines()
            # Strip line terminators.
            result = [s.rstrip() for s in result]
        return result

    def generate_expected(self, backend):
        """
        Generate and return test data output for backend.
        """
        asciidoc = asciidocapi.AsciiDocAPI()
        asciidoc.options.values = self.options
        asciidoc.attributes = self.attributes
        infile = self.source
        outfile = io.StringIO()
        asciidoc.execute(infile, outfile, backend)
        return outfile.getvalue().splitlines()

    def update_expected(self, backend):
        """
        Generate and write backend data.
        """
        lines = self.generate_expected(backend)
        if not os.path.isdir(self.datadir):
            print(('CREATING: %s' % self.datadir))
            os.mkdir(self.datadir)
        with open(self.backend_filename(backend), 'w+', encoding='utf-8') as open_file:
            print(('WRITING: %s' % open_file.name))
            open_file.writelines([s + os.linesep for s in lines])

    def update(self, backend=None, force=False):
        """
        Regenerate and update expected test data outputs.
        """
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        for backend in backends:
            if force or self.is_missing_or_outdated(backend):
                self.update_expected(backend)

    def run(self, backend=None):
        """
        Execute test.
        Return True if test passes.
        """
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        result = True   # Assume success.
        self.passed = self.failed = self.skipped = 0
        print(('%d: %s' % (self.number, self.title)))
        if self.source and os.path.isfile(self.source):
            print(('SOURCE: asciidoc: %s' % self.source))
            for backend in backends:
                fromfile = self.backend_filename(backend)
                skip = False
                for require in self.requires:
                    if shutil.which(require) is None:
                        skip = True
                        break
                if not skip and not self.is_missing(backend):
                    expected = self.get_expected(backend)
                    strip_end(expected)
                    got = self.generate_expected(backend)
                    strip_end(got)
                    lines = []
                    for line in difflib.unified_diff(got, expected, n=0):
                        lines.append(line)
                    if lines:
                        result = False
                        self.failed += 1
                        lines = lines[3:]
                        print(('FAILED: %s: %s' % (backend, fromfile)))
                        message('+++ %s' % fromfile)
                        message('--- got')
                        for line in lines:
                            message(line)
                        message()
                    else:
                        self.passed += 1
                        print(('PASSED: %s: %s' % (backend, fromfile)))
                else:
                    self.skipped += 1
                    print(('SKIPPED: %s: %s' % (backend, fromfile)))
        else:
            self.skipped += len(backends)
            if self.source:
                msg = 'MISSING: %s' % self.source
            else:
                msg = 'NO ASCIIDOC SOURCE FILE SPECIFIED'
            print(msg)
        print('')
        return result


class AsciiDocTests(object):
    def __init__(self, conffile):
        """
        Parse configuration file
        :param conffile:
        """
        self.conffile = conffile
        self.passed = self.failed = self.skipped = 0
        # All file names are relative to configuration file directory.
        self.confdir = os.path.dirname(self.conffile)
        self.datadir = self.confdir  # Default expected files directory.
        self.tests = []              # List of parsed AsciiDocTest objects.
        self.globals = {}
        with open(self.conffile, encoding='utf-8') as open_file:
            lines = Lines(open_file.readlines())
            first = True
            while not lines.eol():
                s = lines.read_until(r'^%+$')
                s = [line for line in s if len(line) > 0]    # Drop blank lines.
                # Must be at least one non-blank line in addition to delimiter.
                if len(s) > 1:
                    # Optional globals precede all tests.
                    if first and re.match(r'^%\s*globals$', s[0]):
                        self.globals = eval(' '.join(normalize_data(s[1:])))
                        if 'datadir' in self.globals:
                            self.datadir = os.path.join(
                                self.confdir,
                                os.path.normpath(self.globals['datadir'])
                            )
                    else:
                        test = AsciiDocTest()
                        test.parse(s[1:], self.confdir, self.datadir)
                        self.tests.append(test)
                        test.number = len(self.tests)
                    first = False

    def run(self, number=None, backend=None):
        """
        Run all tests.
        If number is specified run test number (1..).
        """
        self.passed = self.failed = self.skipped = 0
        for test in self.tests:
            if (not test.disabled or number) and (not number or number == test.number) \
                    and (not backend or backend in test.backends):
                test.run(backend)
                self.passed += test.passed
                self.failed += test.failed
                self.skipped += test.skipped
        if self.passed > 0:
            print(('TOTAL PASSED:  %s' % self.passed))
        if self.failed > 0:
            print(('TOTAL FAILED:  %s' % self.failed))
        if self.skipped > 0:
            print(('TOTAL SKIPPED: %s' % self.skipped))

    def update(self, number=None, backend=None, force=False):
        """
        Regenerate expected test data and update configuratio file.
        """
        for test in self.tests:
            if (not test.disabled or number) and (not number or number == test.number):
                test.update(backend, force=force)

    def list(self):
        """
        Lists tests to stdout.
        """
        for test in self.tests:
            print('%d: %s%s' % (test.number, iif(test.disabled, '!'), test.title))


class Lines(list):
    """
    A list of strings.
    Adds eol() and read_until() to list type.
    """

    def __init__(self, lines):
        super(Lines, self).__init__()
        self.extend([s.rstrip() for s in lines])
        self.pos = 0

    def eol(self):
        return self.pos >= len(self)

    def read_until(self, regexp):
        """
        Return a list of lines from current position up until the next line
        matching regexp.
        Advance position to matching line.
        """
        result = []
        if not self.eol():
            result.append(self[self.pos])
            self.pos += 1
        while not self.eol():
            if re.match(regexp, self[self.pos]):
                break
            result.append(self[self.pos])
            self.pos += 1
        return result


if __name__ == '__main__':
    # guarantee a stable timestamp matching the test fixtures
    os.environ['SOURCE_DATE_EPOCH'] = '1038184662'
    # Process command line options.
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Run AsciiDoc conformance tests specified in '
                                        'configuration FILE.')
    msg = 'Use configuration file CONF_FILE (default configuration file is '\
        'testasciidoc.conf in testasciidoc.py directory)'
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    parser.add_argument('-f', '--conf-file', help=msg)

    subparsers = parser.add_subparsers(metavar='command', dest='command')
    subparsers.required = True

    subparsers.add_parser('list', help='List tests')

    options = ArgumentParser(add_help=False)
    options.add_argument('-n', '--number', type=int, help='Test number to run')
    options.add_argument('-b', '--backend', type=str, help='Backend to run')

    subparsers.add_parser('run', help='Execute tests', parents=[options])

    subparser = subparsers.add_parser('update', help='Regenerate and update test data',
                                      parents=[options])
    subparser.add_argument('--force', action='store_true',
                           help='Update all test data overwriting existing data')

    args = parser.parse_args()

    conffile = os.path.join(os.path.dirname(sys.argv[0]), 'testasciidoc.conf')
    force = 'force' in args and args.force is True
    if args.conf_file is not None:
        conffile = args.conf_file
    if not os.path.isfile(conffile):
        message('missing CONF_FILE: %s' % conffile)
        sys.exit(1)
    tests = AsciiDocTests(conffile)
    cmd = args.command
    number = None
    backend = None
    if 'number' in args:
        number = args.number
    if 'backend' in args:
        backend = args.backend
    if backend and backend not in BACKENDS:
        message('illegal BACKEND: {:s}'.format(backend))
        sys.exit(1)
    if number is not None and (number < 1 or number > len(tests.tests)):
        message('illegal test NUMBER: {:d}'.format(number))
        sys.exit(1)
    if cmd == 'run':
        tests.run(number, backend)
        if tests.failed:
            sys.exit(1)
    elif cmd == 'update':
        tests.update(number, backend, force=force)
    elif cmd == 'list':
        tests.list()
