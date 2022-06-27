from asciidoc import utils
from asciidoc.asciidoc import DEFAULT_NEWLINE, Config, Document, Lex, Macros, Trace
from asciidoc.asciidoc import is_attr_defined, safe, subs_tag, safe_filename
from asciidoc.asciidoc import subs_attrs, system
from asciidoc.attrs import parse_attributes
from asciidoc.exceptions import EAsciiDoc
from asciidoc.message import Message
import os
import re
import sys


UTF8_BOM = b'\xef\xbb\xbf'.decode('utf-8')


class Reader1:
    """Line oriented AsciiDoc input file reader. Processes include and
    conditional inclusion system macros. Tabs are expanded and lines are right
    trimmed."""
    # This class is not used directly, use Reader class instead.
    READ_BUFFER_MIN = 10        # Read buffer low level.

    def __init__(
        self,
        message: Message,
        document: Document,
        macros: Macros,
        config: Config,
    ):
        self.f = None            # Input file object.
        self.fname = None        # Input file name.
        # Read ahead buffer containing [filename,linenumber,linetext] lists.
        self.next = []
        self.cursor = None       # Last read() [filename,linenumber,linetext].
        self.tabsize = 8         # Tab expansion number of spaces.
        self.parent = None       # Included reader's parent reader.
        self._lineno = 0         # The last line read from file object f.
        self.line_ranges = None  # line ranges to include
        self.current_depth = 0   # Current include depth.
        self.max_depth = 10      # Initial maximum allowed include depth.
        self.bom = None          # Byte order mark (BOM).
        self.infile = None       # Saved document 'infile' attribute.
        self.indir = None        # Saved document 'indir' attribute.
        self.message = message
        self.document = document
        self.macros = macros
        self.config = config

    def open(self, fname):
        self.fname = fname
        self.message.verbose('reading: ' + fname)
        if fname == '<stdin>':
            self.f = sys.stdin
            self.infile = None
            self.indir = None
        else:
            self.f = open(fname, 'r', encoding='utf-8')
            self.infile = fname
            self.indir = os.path.dirname(fname)
        self.document.attributes['infile'] = self.infile
        self.document.attributes['indir'] = self.indir
        self._lineno = 0            # The last line read from file object f.
        self.next = []
        # Pre-fill buffer by reading the first line and then pushing it back.
        if self.read():
            if self.cursor[2].startswith(UTF8_BOM):
                self.cursor[2] = self.cursor[2][len(UTF8_BOM):]
                self.bom = UTF8_BOM
            self.unread(self.cursor)
            self.cursor = None

    def closefile(self):
        """Used by class methods to close nested include files."""
        self.f.close()
        self.next = []

    def close(self):
        self.closefile()
        self.__init__()

    def readline(self):
        while True:
            s = self.f.readline()
            if s:
                self._lineno = self._lineno + 1
            else:
                break

            if self.line_ranges is not None:
                for line_range in self.line_ranges:
                    if len(line_range) == 1 and self._lineno == line_range[0]:
                        break
                    elif len(line_range) == 2 and line_range[0] <= self._lineno and \
                            (line_range[1] == -1 or self._lineno <= line_range[1]):
                        break
                else:
                    continue
                break
            else:
                break
        return s

    def read(self, skip=False):
        """Read next line. Return None if EOF. Expand tabs. Strip trailing
        white space. Maintain self.next read ahead buffer. If skip=True then
        conditional exclusion is active (ifdef and ifndef macros)."""
        # Top up buffer.
        if len(self.next) <= self.READ_BUFFER_MIN:
            s = self.readline()
            while s:
                if self.tabsize != 0:
                    s = s.expandtabs(self.tabsize)
                s = s.rstrip()
                self.next.append([self.fname, self._lineno, s])
                if len(self.next) > self.READ_BUFFER_MIN:
                    break
                s = self.readline()
        # Return first (oldest) buffer entry.
        if len(self.next) > 0:
            self.cursor = self.next[0]
            del self.next[0]
            result = self.cursor[2]
            # Check for include macro.
            mo = self.macros.match('+', r'^include[1]?$', result)
            if mo and not skip:
                # Parse include macro attributes.
                attrs = {}
                parse_attributes(mo.group('attrlist'), attrs)
                warnings = attrs.get('warnings', True)
                # Don't process include macro once the maximum depth is reached.
                if self.current_depth >= self.max_depth:
                    self.message.warning('maximum include depth exceeded')
                    return result
                # Perform attribute substitution on include macro file name.
                fname = subs_attrs(mo.group('target'))
                if not fname:
                    return Reader1.read(self)   # Return next input line.
                if self.fname != '<stdin>':
                    fname = os.path.expandvars(os.path.expanduser(fname))
                    fname = safe_filename(fname, os.path.dirname(self.fname))
                    if not fname:
                        return Reader1.read(self)   # Return next input line.
                    if not os.path.isfile(fname):
                        if warnings:
                            self.message.warning('include file not found: %s' % fname)
                        return Reader1.read(self)   # Return next input line.
                    if mo.group('name') == 'include1':
                        if not self.config.dumping:
                            if fname not in self.config.include1:
                                self.message.verbose(
                                    'include1: ' + fname,
                                    linenos=False,
                                )
                                # Store the include file in memory for later
                                # retrieval by the {include1:} system attribute.
                                with open(fname, encoding='utf-8') as f:
                                    self.config.include1[fname] = [
                                        s.rstrip() for s in f
                                    ]
                            return '{include1:%s}' % fname
                        else:
                            # This is a configuration dump, just pass the macro
                            # call through.
                            return result
                # Clone self and set as parent (self assumes the role of child).
                parent = Reader1()
                utils.assign(parent, self)
                self.parent = parent
                # Set attributes in child.
                if 'tabsize' in attrs:
                    try:
                        val = int(attrs['tabsize'])
                        if not val >= 0:
                            raise ValueError('not >= 0')
                        self.tabsize = val
                    except ValueError:
                        raise EAsciiDoc('illegal include macro tabsize argument')
                else:
                    self.tabsize = self.config.tabsize
                if 'depth' in attrs:
                    try:
                        val = int(attrs['depth'])
                        if not val >= 1:
                            raise ValueError('not >= 1')
                        self.max_depth = self.current_depth + val
                    except ValueError:
                        raise EAsciiDoc("include macro: illegal 'depth' argument")
                if 'lines' in attrs:
                    try:
                        if ';' in attrs['lines']:
                            ranges = attrs['lines'].split(';')
                        else:
                            ranges = attrs['lines'].split(',')
                        for idx in range(len(ranges)):
                            ranges[idx] = [int(x) for x in ranges[idx].split('..')]
                        self.line_ranges = ranges
                    except ValueError:
                        raise EAsciiDoc("include macro: illegal 'lines' argument")
                # Process included file.
                self.message.verbose('include: ' + fname, linenos=False)
                self.open(fname)
                self.current_depth = self.current_depth + 1
                result = Reader1.read(self)
        else:
            if not Reader1.eof(self):
                result = Reader1.read(self)
            else:
                result = None
        return result

    def eof(self):
        """Returns True if all lines have been read."""
        if len(self.next) == 0:
            # End of current file.
            if self.parent:
                self.closefile()
                utils.assign(self, self.parent)    # Restore parent reader.
                self.document.attributes['infile'] = self.infile
                self.document.attributes['indir'] = self.indir
                return Reader1.eof(self)
            else:
                return True
        else:
            return False

    def read_next(self):
        """Like read() but does not advance file pointer."""
        if Reader1.eof(self):
            return None
        else:
            return self.next[0][2]

    def unread(self, cursor):
        """Push the line (filename,linenumber,linetext) tuple back into the read
        buffer. Note that it's up to the caller to restore the previous
        cursor."""
        assert cursor
        self.next.insert(0, cursor)


class Reader(Reader1):
    """ Wraps (well, sought of) Reader1 class and implements conditional text
    inclusion."""
    def __init__(
        self,
        message: Message,
        document: Document,
        macros: Macros,
        config: Config,
    ):
        Reader1.__init__(self, message, document, macros, config)
        self.depth = 0          # if nesting depth.
        self.skip = False       # true if we're skipping ifdef...endif.
        self.skipname = ''      # Name of current endif macro target.
        self.skipto = -1        # The depth at which skipping is re-enabled.

    def read_super(self):
        result = Reader1.read(self, self.skip)
        if result is None and self.skip:
            raise EAsciiDoc('missing endif::%s[]' % self.skipname)
        return result

    def read(self):
        result = self.read_super()
        if result is None:
            return None
        while self.skip:
            mo = self.macros.match('+', r'ifdef|ifndef|ifeval|endif', result)
            if mo:
                name = mo.group('name')
                target = mo.group('target')
                attrlist = mo.group('attrlist')
                if name == 'endif':
                    self.depth -= 1
                    if self.depth < 0:
                        raise EAsciiDoc('mismatched macro: %s' % result)
                    if self.depth == self.skipto:
                        self.skip = False
                        if target and self.skipname != target:
                            raise EAsciiDoc('mismatched macro: %s' % result)
                else:
                    if name in ('ifdef', 'ifndef'):
                        if not target:
                            raise EAsciiDoc('missing macro target: %s' % result)
                        if not attrlist:
                            self.depth += 1
                    elif name == 'ifeval':
                        if not attrlist:
                            raise EAsciiDoc('missing ifeval condition: %s' % result)
                        self.depth += 1
            result = self.read_super()
            if result is None:
                return None
        mo = self.macros.match('+', r'ifdef|ifndef|ifeval|endif', result)
        if mo:
            name = mo.group('name')
            target = mo.group('target')
            attrlist = mo.group('attrlist')
            if name == 'endif':
                self.depth = self.depth - 1
            else:
                if not target and name in ('ifdef', 'ifndef'):
                    raise EAsciiDoc('missing macro target: %s' % result)
                defined = is_attr_defined(target, self.document.attributes)
                if name == 'ifdef':
                    if attrlist:
                        if defined:
                            return attrlist
                    else:
                        self.skip = not defined
                elif name == 'ifndef':
                    if attrlist:
                        if not defined:
                            return attrlist
                    else:
                        self.skip = defined
                elif name == 'ifeval':
                    if safe():
                        self.message.unsafe('ifeval invalid')
                        raise EAsciiDoc('ifeval invalid safe document')
                    if not attrlist:
                        raise EAsciiDoc('missing ifeval condition: %s' % result)
                    cond = False
                    attrlist = subs_attrs(attrlist)
                    if attrlist:
                        try:
                            cond = eval(attrlist)
                        except Exception as e:
                            raise EAsciiDoc(
                                'error evaluating ifeval condition: %s: %s' % (
                                    result,
                                    str(e)
                                )
                            )
                        self.message.verbose('ifeval: %s: %r' % (attrlist, cond))
                    self.skip = not cond
                if not attrlist or name == 'ifeval':
                    if self.skip:
                        self.skipto = self.depth
                        self.skipname = target
                    self.depth = self.depth + 1
            result = self.read()
        if result:
            # Expand executable block macros.
            mo = self.macros.match('+', r'eval|sys|sys2', result)
            if mo:
                action = mo.group('name')
                cmd = mo.group('attrlist')
                result = system(action, cmd, is_macro=True)
                self.cursor[2] = result  # So we don't re-evaluate.
        if result:
            # Un=escape escaped system macros.
            if self.macros.match('+', r'\\eval|\\sys|\\sys2|\\ifdef|\\ifndef|\\endif|\\include|\\include1', result):  # noqa=E501
                result = result[1:]
        return result

    def eof(self):
        return self.read_next() is None

    def read_next(self):
        save_cursor = self.cursor
        result = self.read()
        if result is not None:
            self.unread(self.cursor)
            self.cursor = save_cursor
        return result

    def read_lines(self, count=1):
        """Return tuple containing count lines."""
        result = []
        i = 0
        while i < count and not self.eof():
            result.append(self.read())
        return tuple(result)

    def read_ahead(self, count=1):
        """Same as read_lines() but does not advance the file pointer."""
        result = []
        putback = []
        save_cursor = self.cursor
        try:
            i = 0
            while i < count and not self.eof():
                result.append(self.read())
                putback.append(self.cursor)
                i = i + 1
            while putback:
                self.unread(putback.pop())
        finally:
            self.cursor = save_cursor
        return tuple(result)

    def skip_blank_lines(self):
        self.read_until(r'\s*\S+')

    def read_until(self, terminators, same_file=False):
        """Like read() but reads lines up to (but not including) the first line
        that matches the terminator regular expression, regular expression
        object or list of regular expression objects. If same_file is True then
        the terminating pattern must occur in the file the was being read when
        the routine was called."""
        if same_file:
            fname = self.cursor[0]
        result = []
        if not isinstance(terminators, list):
            if isinstance(terminators, str):
                terminators = [re.compile(terminators)]
            else:
                terminators = [terminators]
        while not self.eof():
            save_cursor = self.cursor
            s = self.read()
            if not same_file or fname == self.cursor[0]:
                for reo in terminators:
                    if reo.match(s):
                        self.unread(self.cursor)
                        self.cursor = save_cursor
                        return tuple(result)
            result.append(s)
        return tuple(result)


class Writer:
    """Writes lines to output file."""
    def __init__(self, message: Message, trace: Trace, config: Config):
        self.newline = DEFAULT_NEWLINE   # End of line terminator.
        self.f = None                    # Output file object.
        self.fname = None                # Output file name.
        self.lines_out = 0               # Number of lines written.
        self.skip_blank_lines = False    # If True don't output blank lines.
        self.message = message
        self.trace = trace
        self.config = config

    def open(self, fname, bom=None):
        """
        bom is optional byte order mark.
        http://en.wikipedia.org/wiki/Byte-order_mark
        """
        self.fname = fname
        if fname == '<stdout>':
            self.f = sys.stdout
        else:
            self.f = open(fname, 'w+', encoding='utf-8', newline="")
        self.message.verbose('writing: ' + self.fname, False)
        if bom:
            self.f.write(bom)
        self.lines_out = 0

    def close(self):
        if self.fname != '<stdout>':
            self.f.close()

    def write_line(self, line=None):
        if not (self.skip_blank_lines and (not line or not line.strip())):
            # Replace out any escaped attributes with non-escaped versions
            self.f.write((re.sub(r'\\({[a-zA-Z0-9_][a-zA-Z0-9_\-]*)', '\\1', line) or '') + self.newline)  # noqa=E501
            self.lines_out = self.lines_out + 1

    def write(self, *args, **kwargs):
        """Iterates arguments, writes tuple and list arguments one line per
        element, else writes argument as single line. If no arguments writes
        blank line. If argument is None nothing is written. self.newline is
        appended to each line."""
        if 'trace' in kwargs and len(args) > 0:
            self.trace(kwargs['trace'], args[0])
        if len(args) == 0:
            self.write_line()
            self.lines_out = self.lines_out + 1
        else:
            for arg in args:
                if utils.is_array(arg):
                    for s in arg:
                        self.write_line(s)
                elif arg is not None:
                    self.write_line(arg)

    def write_tag(self, tag, content, subs=None, d=None, **kwargs):
        """Write content enveloped by tag.
        Substitutions specified in the 'subs' list are perform on the
        'content'."""
        if subs is None:
            subs = self.config.subsnormal
        stag, etag = subs_tag(tag, d)
        content = Lex.subs(content, subs)
        if 'trace' in kwargs:
            self.trace(kwargs['trace'], [stag] + content + [etag])
        if stag:
            self.write(stag)
        if content:
            self.write(content)
        if etag:
            self.write(etag)
