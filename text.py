# (c) Eugene M. Minkovskii; text.py 07 Dec 2003
# emin(at)mccme(point)ru

## GPL           #################################{{{1
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
## }}}

"""\
This is text.py module for easy association of vim buffer to python language.
Module provides Text-calss, which has access vim buffer contents, and has many
of string, sequense and file-object methods. You may use slice, may use
assignment to slice of buffer, and you can use step argument in this assignment
in python 2.3 notation. You can use all of string methods like .upper(),
.lower(), .center() etc. You can use many of sequence methods like .append(),
.extend(), .reverse() etc. You can use a lot of binary operators like +=, *=;
membership test "in" etc. Moreover, Text-instance provide some facilities to
work with regular expressions including situations when text in buffer is in
multibyte encoding. Searching takes place in unicode, but module provides some
new match object: "NoUniMatchObj". This object has all of original match
objects attributes but when you expect to get a string, you get a string not
unicode. And when you expect to get address (byte-offset) you get address in
encoded string too.

Simple example:
~~~~~~~~~~~~~~~
import text
t = text.Text()
for i in t.re.finditer(my_regexp):    # search my_regexp in buffer
    try:
        t.replace_i(i.start(),            # interactive replace fragment of
                    i.end(),              #   buffer from i.start() to i.end()
                                          #   where i is an instance of
                                          #   NoUniMatchObj
                    ["replasement one",   # There are a lot of substitutions,
                     my_function(i), ...])#   user can choose one of them.
    except t.exceptions.CancelDialog:
        pass                            # handler of Cancel button
t.center(80)                            # centering contents of buffer
t.apply_to_lines(my_other_function)     # apply my_other_function line by line
"""

## Installation  #################################{{{1
#
# 1) Make in your harddrive some directory for python-vim programs (let it name
#    is /pythonvim/). And put text.py into this directory.
# 2) Instract python to use this directory like sourse of modules. One way to
#    do this is put following string into your .vimrc file:
# :py import sys; sys.path.insert(0, r"/pythonvim/")
#    NOTE: in some systems you must put absolute address into sys.path list.
#    NOTE: be careful about slash direction, this is system-depended.
#
# That is all. Happy vimming.
#
# Compatibility note: {{{2
#
# This program writen for Python 2.3. But it is already compatible with
# Python 2.2. And for compatibility with Python 2.1 you may do some actions:
# some code need to be comment and some to uncomment.
#
# For compatibility with python 2.1 open this program in vim and execute
#   following command:
# :%s/^\(\s*\)\(.*#<p21c>\)$/\1## \2/|%s/^\(\s*\)##\s\+\(.*#<p21u>\)$/\1\2/|w!
# Be careful, use copy&paste:
#       1) put cursor after the colon and type y$
#       2) Then type : to go into command line and type <C-R>"
# This command comment section using 'yield' statement and import generators
#   feature. Then it is uncomment compatibility blocks: raise instraction in
#   finditer() method and import nested_scopes feature.
# For undoing this changes execute in vim following command:
# :%s/^\(\s*\)\(.*#<p21u>\)$/\1## \2/|%s/^\(\s*\)##\s\+\(.*#<p21c>\)$/\1\2/|w!
## }}}
## }}}
## Change log    #################################{{{1
#
# NOTE: -- FIRST   number changed when I rewrite kernel of program
#       -- SECOND, when I change user interface, adding new "greate" method
#       -- THIRD,  little bugfix, or adding/rewriting self-documentation,
#          or just put some comment in script. Not of all of this little
#          changes need to describe in this section.
#
# 1.0.4 -- Some spell check of documentation. Thanks to all helpers.
#          new raise instractions with some help for developers.
#          Bugfix in re.subn() method.
# 1.0.3 -- A lot of bugfix. If user use unknown for python 'encoding', script
#          try to search substitution in some dictionary, and made some
#          warnings and exceptions.
# 1.0.2 -- Compatibility with python 2.1 tested and bugfixed, instarction how
#          to turn it on you can see in installation instructions. Rename
#          _AdvancedMO object into NoUniMatchObj, because it may be imported
#          into other prgrams. Bugfix in .group() method of NoUniMatchObj
#          object. More Documentation.
# 1.0.1 -- Compatibility with python 2.1 restored, but after some action
#          described in installation guide. A little bugfix in NoUniMatchObj()
#          class. Bugfix in compatibility with python 2.2 block. I was tested
#          some important methods in Linux RedHat 8.0 python 2.2 vim 6.1
# 1.0.0 -- 1) Change internal representation of text. Now internal object not
#          in unicode. This is not comfortable for vim.
#          2) Killing back compatibility with python 2.1: python 2.2 required;
#          pyhton 2.3 recommended.
#          3) Now setitem supported step argument
#          (text_obj=[start:stop:step]=sequence)
#          4) three new methods adding: insert(), remove() and reverse().
#          There are no more FIXME mark in program, but have some TODO: no
#          sort() and pop() methods. New class NoUniMatchObj() need
#          documentation.
# 0.2.1 -- Back compatibility block. Warning! This module now already
#          compilable under python 2.1 and I was test some functions (like
#          Text.center()).  But more powerfull test I don't do.
# 0.2.0 -- I found greatest bug in my program when they try to work with
#          multibyte encoding. This bug force me to rewrite many methods which
#          use expressly or by implication +byte_offset feature by vim. Now
#          working of this script don't depend off availability of +byte_offset
#          feature in vim. There are two new methods provide for access to real
#          byte-offset in vim: Text.offset2LC() and Text.LC2offset()
#          NOTE: later, in version 1.0.0, I rewrite this again. :(
# 0.1.4 -- new interaction method: replace_i(); New containers with exceptions
#          and buttons
# 0.1.3 -- now all of _RegExp using unicode flag for compile the pattern adding
#          decode() method (just return self.text). __str__() and encode()
#          methods now automatically use self.encoding to encode self.text.
#          Writing documentation
# 0.1.2 -- improvement interactive() method
# 0.1.0 -- adding interactive() method
# 0.0.0 -- initial version: support mutable string and file methods, version
#          info, _RegExp subclass with addition count() method. All working
#          good (I'm hope). A lot of known bugs marked in the script by FIXME
#          comment
## }}}

## import part   #################################{{{1

from __future__ import generators       # for python 2.2        #<p21c>
## from __future__ import nested_scopes # for python 2.1        #<p21u>
try: import vim
except ImportError:
    raise ImportError("This module available only from Vim editor")
if not int(vim.eval('has("byte_offset")')):
    raise "Bad vim version: need +byte_offset feature"
import re, locale, sys, traceback

## }}}
## Constants     #################################{{{1
## back comatibility with old Python versions (no warranty) ##{{{2

if sys.hexversion < 0x2030000:          # python 2.2
    def enumerate(seq):
        return zip(xrange(len(seq)),seq)
    def bool(obj):
        if obj: return True
        else:   return False
    if sys.hexversion >= 0x2020000:     # python 2.2 but not 2.1
        import __builtin__
        basestring = "basestring"
        def isinstance(obj, _type):
            if _type == basestring:
                return  __builtin__.isinstance(obj, str) or\
                        __builtin__.isinstance(obj, unicode)
            else: return __builtin__.isinstance(obj, _type)
    if sys.hexversion < 0x2020000:      # python 2.1
        class object: pass
        basestring = "basestring"
        import types
        def isinstance(obj, _type):
            if _type == basestring:
                return type(obj) in [types.StringType, types.UnicodeType]
            elif _type == int:
                return type(obj) in [types.IntType, types.LongType]
            elif _type == unicode:
                return type(obj) ==  types.UnicodeType
            elif _type == str:
                return type(obj) ==  types.StringType
            elif _type == tuple:
                return type(obj) ==  types.TupleType
            else:
                raise "New bag: isinstance cant chek type of %r object"%obj
        True  = 1
        False = 0

## }}}

__version__ = (1, 0, 4)
__all__ = ["Text", "NoUniMatchObj",                               # classes
           "YES", "NO", "OTHER", "CANCEL", "BREAK",               # buttons
           "VERSION", "VERSION_INFO", "HEXVERSION", "VIMVERSION", # versions
           "BreakDialog", "CancelDialog", "OtherDialog"]          # exceptions
VERSION = "text module %i.%i.%i provide Python interface for Vim.\n"\
          "Python 2.2 compatible, but Python 2.3 recommended.\n"\
          "Python 2.1 may be used after some action\n"\
          "(see installation instructions)"%__version__[0:3]
## VERSION = VERSION + ".\nBack compatibility mode turning on." #<p21u>
VERSION_INFO = __version__
HEXVERSION   = __version__[0]*(16**4)+__version__[1]*(16**2)+__version__[2]
VIMVERSION   = int(vim.eval("v:version"))
YES    =  2 # 2**1
NO     =  4 # 2**2
OTHER  =  8 # 2**3
CANCEL = 16 # 2**4
BREAK  = 32 # 2**5
class _button_container(object):
    "This is class-container"
    YES    = YES
    NO     = NO
    OTHER  = OTHER
    CANCEL = CANCEL
    BREAK  = BREAK
_IS_DIALOG_ENABLED = bool(int(vim.eval("has('dialog_con')")) or\
        int(vim.eval("has('dialog_gui')")))

## }}}
## AuxFunc       #################################{{{1

def _true_offset(u_obj, offset, encoding, prev=(0,0)):
    return len(u_obj[prev[0]:offset].encode(encoding)) + prev[1]
    # prev - offset in previouse known point: (u_offs,true_offs)
def _encode_if_u(obj, encoding):
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    else: return obj
def _print_warning(string):
    vim.command('echohl WarningMsg | echo "%s" | echohl None'%string)

## }}}
## Exceptions    #################################{{{1

class BreakDialog(Exception):
    pass

class CancelDialog(Exception):
    pass

class OtherDialog(Exception):
    pass

class _ExceptionsContainer(object):
    "This is class-container"
    BreakDialog  = BreakDialog
    CancelDialog = CancelDialog
    OtherDialog  = OtherDialog

## }}}
## NoUniMatchObj #################################{{{1

class NoUniMatchObj(object):
    ## Documentation {{{2
    """\
    NoUniMatchObj(match_object, encoding [, oldNoUniMatchObj_object]) ->
    -> NoUniMatchObj_object

    If we make regexp search in unicode string by means of standart module re,
    it return sometime MATCH_OBJECT, which provide access to many useful
    information. But this is information about unicode string in which we do
    search. For work with vim buffers information about string in vim encoding
    is more useful. So, this class provide object-emulator of standart
    MATCH_OBJECT. When you expect to get a string, you get a string in ENCODING
    not unicode. And when you expect to get address (byte-offset) you get
    address in encoded string too. The last is important if you use multibyte
    encoding especially encoding which may represent various symbol by byte
    various length (utf-8 for example).

    MATCH_OBJECT --- true match_object returned by re module.
    ENCODING     --- encoding for convertation
    OLD_ADVANCEDMO_OBJECT --- optional, default None. This is useful for swift
    initialization. If you already do some search in current unicode object by
    current regular expression, some attribute may be copyed from previous
    _ADVANSEDMO_OBJECT. For example, this is useful for finditer() method.

    ------------------------------------------------------------------------
    Data:								*NoUniMatchObj-data*

    mo        # true (may be unicode) match object
    encoding  # encoding for convert unicode objects
    lastindex # The integer index of the last matched capturing group, or None
                if no group was matched at all. This is same as mo.lastindex.
                (see documentation for module re)
    lastgroup # The name of the last matched capturing group, or None if the
                group didn't have a name, or if no group was matched at all.
                This is same as mo.lastgroup. (see documentation for module re)
    re        # The regular expression object whose match() or search() method
                produced this MatchObject instance. This is same as mo.re.
    string    # The string passed to match() or search(). This is similar as mo.re,
                but converted into encoding if mo.re is unicode object.
    pos       # The value of pos which was passed to the search() or match()
                method. This is the index into the string at which the RE
                engine started looking for a match. This is similar as mo.pos,
                but corrected if mo.string is unicode object like describe
                above.
    endpos    # The value of endpos which was passed to the search() or match()
                method of the RegexObject. This is the index into the string
                beyond which the RE engine will not go. This is similar as
                mo.endpos, but corrected if mo.string is unicode object like
                describe above.

    ------------------------------------------------------------------------
    Methods:								*NoUniMatchObj-methods*

        List of NoUniMatchObj methods: expand(), group(), groups(), groupdict(),
            start(), end(), span()
    """
    ## }}}
    mo        = None
    lastindex = None
    lastgroup = None
    re        = None
    string    = None
    pos       = None
    endpos    = None
    encoding  = None
    def __init__(self, mo, encoding, old_mo = None):
        if old_mo:
            for i in ["string", "pos", "endpos"]:
                setattr(self,i,getattr(old_mo,i))
        else:
            if isinstance(mo.string, unicode):
                self.pos    = _true_offset(mo.string, mo.pos,    encoding)
                self.endpos = _true_offset(mo.string, mo.endpos, encoding,
                        (mo.pos, self.pos))
                self.string = mo.string.encode(encoding)
            else:
                self.pos    = mo.pos
                self.endpos = mo.endpos
                self.string = mo.string
        self.encoding  = encoding
        self.mo        = mo
        self.lastindex = mo.lastindex
        self.lastgroup = mo.lastgroup
        self.re        = mo.re

    def expand(self, template):
        """\
        expand(template) -> string

        Return the string obtained by doing backslash substitution on the
        template string template, as done by the sub() method. Escapes such as
        "\\n" are converted to the appropriate characters, and numeric
        backreferences ("\\1", "\\2") and named backreferences ("\\g<1>",
        "\\g<name>") are replaced by the contents of the corresponding group. 

        Always return string, not unicode.
        """        
        result = self.mo.expand(temlate)
        return _encode_if_u(result, self.encoding)

    def group(self, *gr):
        """\
        group([group1, ...]) -> string or tuple of strings

        Returns one or more subgroups of the match. If there is a single
        argument, the result is a single string; if there are multiple
        arguments, the result is a tuple with one item per argument. Without
        arguments, group1 defaults to zero (the whole match is returned). If a
        groupN argument is zero, the corresponding return value is the entire
        matching string; if it is in the inclusive range [1..99], it is the
        string matching the corresponding parenthesized group. If a group
        number is negative or larger than the number of groups defined in the
        pattern, an IndexError exception is raised. If a group is contained in
        a part of the pattern that did not match, the corresponding result is
        None. If a group is contained in a part of the pattern that matched
        multiple times, the last match is returned.  If the regular expression
        uses the (?P<name>...) syntax, the groupN arguments may also be strings
        identifying groups by their group name. If a string argument is not
        used as a group name in the pattern, an IndexError exception is raised. 

        Always return string or tuple of strings, not unicode.
        """
        result = self.mo.group(*gr)
        if isinstance(result,tuple):
            return tuple(map(lambda x: _encode_if_u(x, self.encoding)))
        else:
            return _encode_if_u(result, self.encoding)

    def groups(self, default=None):
        """\
        groups([defualt]) -> tuple

        Return a tuple containing all the subgroups of the match, from 1 up to
        however many groups are in the pattern. The default argument is used
        for groups that did not participate in the match; it defaults to None.

        Always return tuple of strings, not of unicode.
        """
        result = self.mo.groups(default)
        return tuple(map(lambda x: _encode_if_u(x, self.encoding), result))

    def groupdict(self, default=None):
        """\
        groupdict([default]) -> dict

        Return a dictionary containing all the named subgroups of the match,
        keyed by the subgroup name. The default argument is used for groups
        that did not participate in the match; it defaults to None.

        All keys and values are string, not unicode.
        """
        result = {}
        for i in self.mo.groupdict.keys():
            result[_encode_if_u(i, self.encoding)] =\
                    _encode_if_u(self.mo.groupdict(default)[i], self.encoding)
        return result

    def start(self, gr=0):
        """\
        start([group]) -> int

        Return the index of the start of the substring matched by GROUP; GROUP
        defaults to zero (meaning the whole matched substring).  Return -1 if
        GROUP exists but did not contribute to the match.

        If search made in unicode, return offset like allegedly search made in
        string.
        """
        if isinstance(self.mo.string, unicode):
            return _true_offset(self.mo.string, self.mo.start(gr), self.encoding)
        else:
            return self.mo.start(gr)

    def end(self, gr=0):
        """\
        end([group]) -> int

        Return the index of the end of the substring matched by GROUP; GROUP
        defaults to zero (meaning the whole matched substring).  Return -1 if
        GROUP exists but did not contribute to the match.

        If search made in unicode, return offset like allegedly search made in
        string.
        """
        if isinstance(self.mo.string, unicode):
            return _true_offset(self.mo.string, self.mo.end(gr),   self.encoding)
        else:
            return self.mo.end(gr)

    def span(self, gr=0):
        """\
        span([group]) -> tuple

        For NoUniMatchObj object m, return the 2-tuple (m.start(group),
        m.end(group)).  Note that if group did not contribute to the match,
        this is (-1, -1).  Again, group defaults to zero. 

        If search made in unicode, return offset like allegedly search made in
        string.
        """
        if isinstance(self.mo.string, unicode):
            start = self.start(gr)
            end   = start + len(self.group(gr))
            return start, end
        else:
            return self.mo.span(gr)

## }}}
## _RegExp       #################################{{{1

class _RegExp(object):
    "This is class-container"

    def __init__(self, master):
        self.master = master

    def compile(self, pattern, flags=0):
        """\
        re.compile(pattern [, flags]) -> RegExp_object

        Compile a regular expression pattern into a regular expression object.
        The expression's behaviour can be modified by specifying a FLAGS value.
        Values can be any of standart constants of module re, combined using
        bitwise OR (the | operator). This method always put re.UNICODE to the
        FLAGS.
        """

        if isinstance(pattern, basestring):
            if not isinstance(pattern, unicode) and\
                    re.search(r"[\x80-\xff]",pattern):
                raise re.sub("(?m)^", " |  ",
                    "You pass to compile method string which must be convert\n"\
                    "into unicode.  I can't do this automatically because\n"\
                    "I can't guess what codec you need: may be it is vim\n"
                    "'encoding' variable (%s), may be vim 'fileencoding'\n"
                    "variable (%s), may be your script encoding,\n"
                    "may be something else..."%(
                        self.master.encoding,
                        vim.eval("&fileencoding")))
            return re.compile(pattern, flags|re.U)
        elif pattern.flags == (pattern.flags|re.U):
            return pattern
        else:
            return re.compile(pattern.pattern, flags|re.U)

    def search(self, pattern, flags=0, *pos):
        """\
        re.search(pattern [, flags [, pos [, endpos]]]) -> NoUniMatchObj_object

        Scan through buffer looking for a location where the regular expression
        pattern produces a match, and return a corresponding NoUniMatchObj object
        instance. Return None if no position in the string matches the pattern;
        note that this is different from finding a zero-length match at some
        point in the string. 
        """
        pattern = self.compile(pattern, flags)
        mo = NoUniMatchObj(pattern.search(self.master.decode(),*pos),
                self.master.encoding)
        return mo

    def match(self, pattern, flags=0, *pos):
        """\
        re.match(pattern [, flags [, pos [, endpos]]]) -> NoUniMatchObj_object

        If zero or more characters at the beginning of buffer match this
        regular expression, return a corresponding NoUniMatchObj instance. Return
        None if the string does not match the pattern; note that this is
        different from a zero-length match. 

        NOTE: If you want to locate a match anywhere in string, use re.search()
        instead. 

        The optional parameter POS gives an index in the string where
        the search is to start; it defaults to 0. This is not completely
        equivalent to slicing the string; the "^" pattern character matches at
        the real beginning of the string and at positions just after a newline,
        but not necessarily at the index where the search is to start. 

        The optional parameter ENDPOS limits how far the string will be
        searched; it will be as if the string is endpos characters long, so
        only the characters from POS to ENDPOS - 1 will be searched for a
        match. If endpos is less than pos, no match will be found.
        """
        pattern = self.compile(pattern, flags)
        mo = NoUniMatchObj(pattern.match(self.master.decode(),*pos),
                self.master.encoding)
        return mo

    def split(self, pattern, maxsplit=0):
        """\
        re.split(pattern [, maxsplit]) -> list

        Split buffer content by the occurrences of pattern. If capturing
        parentheses are used in pattern, then the text of all groups in the
        pattern are also returned as part of the resulting list. If MAXSPLIT is
        nonzero, at most maxsplit splits occur, and the remainder of the string
        is returned as the final element of the list.
        """

        pattern = self.compile(pattern)
        result  = re.split (pattern, self.master.decode(), maxsplit)
        return map(lambda x: _encode_if_u(x, self.master.encoding),
                result)

    def findall(self, pattern):
        """\
        re.findall(pattern) -> list

        Return a list of all non-overlapping matches of pattern in buffer. If
        one or more groups are present in the pattern, return a list of groups;
        this will be a list of tuples if the pattern has more than one group.
        Empty matches are included in the result unless they touch the
        beginning of another match. 
        """

        pattern = self.compile(pattern)
        result  = re.findall(pattern, self.master.decode())
        return map(lambda x: _encode_if_u(x, self.master.encoding),
                result)

    def finditer(self, pattern):
        """\
        re.finditer(pattern) -> iterator_object

        Return an iterator over all non-overlapping matches for the RE pattern
        in string. For each match, the iterator returns an NoUniMatchObj object.
        Empty matches are included in the result unless they touch the
        beginning of another match. Not availabel in python 2.1
        """

        if sys.hexversion < 0x2020000:          # for python 2.1
            raise "Too old python for work with generators: 2.2 or later required"
        pattern = self.compile(pattern)
        old_mo  = None
        for i in re.finditer(pattern, self.master.decode()):
            mo = NoUniMatchObj(i, self.master.encoding, old_mo)
            old_mo = mo
            yield mo                                            #<p21c>

    def count(self, pattern):
        """\
        re.count(pattern) -> int

        Return number of occurences. Note: module re has not this function
        """

        pattern = self.compile(pattern)
        return len(map(None, pattern.finditer(self.master.decode())))

    def sub(self, pattern, repl, *count):
        """\
        re.sub(pattern, repl [, count]) -> None

        Change buffer by replacing the leftmost non-overlapping occurrences of
        PATTERN in buffer by the replacement REPL. REPL can be a string (in
        unicode) or a function; if it is a string, any backslash escapes in it
        are processed.  That is, "\\n" is converted to a single newline
        character, "\\r" is converted to a linefeed, and so forth. Unknown
        escapes such as "\\j" are left alone. Backreferences, such as "\\6",
        are replaced with the substring matched by group 6 in the PATTERN.

        If REPL is a function, it is called for every non-overlapping
        occurrence of pattern. The function takes a single match object
        argument, and returns the replacement string in unocode.

        The optional argument COUNT is the maximum number of pattern
        occurrences to be replaced; COUNT must be a non-negative integer.
        If omitted or zero, all occurrences will be replaced.

        NOTE 1: really search made in unicode string, your REPL mast return
        unicode or 7-bit string.
        NOTE 2: match object pass to the function REPL, not NoUniMatchObj.
        If you need to use NoUniMatchObj in function, use re.finditer() method.
        """

        pattern = self.compile(pattern)
        try:
            result = re.sub(pattern, repl, self.master.decode(), *count)
        except UnicodeDecodeError:
            traceback.print_exc()
            raise re.sub("(?m)^", " |  ",
                "You pass to substitute method string or function\n"\
                "which return string, not unicode.  But substitutions\n"\
                "really made in unicode and I can't guess what codec\n"\
                "you need: may be it is vim 'encoding' variable (%s),\n"\
                "may be vim 'fileencoding' variable (%s),\n"\
                "may be your script encoding, may be something else..."%(
                        self.master.encoding,
                        vim.eval("&fileencoding")))
        self.master.text = result.encode(self.master.encoding)
        self.master.update_py2vi()

    def subn(self, pattern, repl, *count):
        """\
        re.subn(pattern, repl [, count]) -> int

        Perform the same operation as sub(), but return number of
        substitutions made.
        """

        pattern = self.compile(pattern)
        try:
            result, n = re.subn(pattern, repl, self.master.decode(), *count)
        except UnicodeDecodeError:
            traceback.print_exc()
            raise re.sub("(?m)^", " |  ",
                "You pass to substitute method string or function\n"\
                "which return string, not unicode.  But substitutions\n"\
                "really made in unicode and I can't guess what codec\n"\
                "you need: may be it is vim 'encoding' variable (%s),\n"\
                "may be vim 'fileencoding' variable (%s),\n"\
                "may be your script encoding, may be something else..."%(
                        self.master.encoding,
                        vim.eval("&fileencoding")))
        self.master.text = result.encode(self.master.encoding)
        self.master.update_py2vi()
        return n

## }}}
## Text          #################################{{{1

class Text(object):
    ## Documentation and version information {{{2

    """\
    Text([vim_buffer]) -> <text.Text object>

    This class provides simple access to vim buffer from python.  Constractor
    take one optional argument---vim's buffer (default is the current buffer).
    instance = text.Text()       # see `instance' below in examples

    Buffer contents store in instance.text attribute in vim internal encodind
    (see 'encoding' option in vim). Because python don't know about what is
    letter and how case convert in many encodings if it is not locale turn on
    (note: many encodings on many systems has no locale for it), we convert
    buffer contents in unicode when it is necessary. But as rule we do it in
    shadow and user don't see it, except we work with regular expressions (see
    below).

    ------------------------------------------------------------------------
    Synchronization and Offset methods:				*synchronization-methods*
    								*offset-methods*

        General synchronization methods: update_vi2py(), update_py2vi()

        Offset converting methods: offset2LC(), LC2offset()

    ------------------------------------------------------------------------
    String emulation:						*string-methods*

    Instance of this class has most of string methods. Some of them (like
    isdigit() etc.) work similarly as in the string, but others, which return
    changed string, really return None and modify the buffer line-by-line.

        List of string methods: count(), index(), find(), rindex(), rfind(),
            endswith(), statswith(), isalnum(), isalpha(), isdigit(),
            islower(), isspace(), istitle(), isupper(), center(), rjust(),
            ljust(), zfill(), rstrip(), lstrip(), strip(), capitalize(),
            lower(), swapcase(), title(), upper(), replace(), expandtabs(),
            decode(), encode(), split(), splitlines()

        Non standart string methods: apply_to_lines()

    ------------------------------------------------------------------------
    Sequence emulation:						*sequence-methods*

    Instance of this class has a lot of sequence's methods and can properly
    work with a slice. For example:
    string = instance[start:end:step] # return substring
    instance[start:end] = "string"    # record "string" into start:end area
    instance[start:end:step] = list   # new in 1.0.0 but only since python 2.3
    instance += "string"              # append string
    instance *= Int                   # multiplicate buffer

        List of sequence methods: __setitem__(), __delitem__(), __getitem__(),
            __len__(), __contains__(), __iadd__(), append(), extend(),
            __imul__(), insert(), remove(), reverse()

    ------------------------------------------------------------------------
    File emulation:						*file-methods*

    Instance of this class has a lot of file-object methods and may be used for
    emulation file-object. For example:
    sys.stdout = instance     # STDOUT redirection

        List of file methods: isatty(), close(), flush(), tell(), seek(),
            truncate(), read(), readline(), readlines(), write(), writelines()

        List of file attributes: closed, mode, newlines, name, encoding

    ------------------------------------------------------------------------
    RegExp access:						*RegExp-methods*

    For working whith regular expressions class provide re subclass with most
    or regexp functions:
    instance.re.match(), instance.re.search(), instance.re.finditer(),
    instance.re.sub() etc.  and addition instance.re.count() method, which not
    provide by the re module.

    NOTE: class has two different methods: self.count() and self.re.count().

    NOTE: when this methods called, python convert buffer contains into
    unicode (see above) and make search in it, flag re.U pass to pattern
    automatically (That is recompiled if necessary).

    Important:
    But we redefine match object so that return offset as if search made in vim
    internal encoding (this is importatn in multibyte encodings). Moreover,
    methods like group() return strings in vim internal encoding, not in
    unicode. But if you need to get original "true" match object, thay stored
    in "mo" attribute. See NoUniMatchObj() class documentation.

    WARNING: we can't guess the encoding used by your program, therefore we
    don't automatically convert the pattern into unicode. Please do this
    yourself if it is necesary.

        List of RegExp methods: re.compile(), re.search(), re.match(),
            re.split(), re.findall(), re.finditer(), re.sub(), re.subn()

        Non standart RegExp methods: re.count()

    ------------------------------------------------------------------------
    Vim intaraction:						*interactive-methods*

    Class provide some methods to interactive actions.

        List of interaction methods: interactive(), replace_i()
    
    ------------------------------------------------------------------------
    Exceptions:							*text-exceptions*

    instance.exceptions              # Exceptions container: has an attributes:
    instance.exceptions.BreakDialog  # using in replace_i() method
    instance.exceptions.CancelDialog # using in replace_i() method
    instance.exceptions.OtherDialog  # using in replace_i() method

    ------------------------------------------------------------------------
    Buttons:							*text-buttons*

    instance.buttons          # Buttons container: has an attributes:
    instance.buttons.YES
    instance.buttons.NO
    instance.buttons.OTHER
    instance.buttons.CANCEL
    instance.buttons.BREAK

    ------------------------------------------------------------------------
    Other data:							*text-attributes*

    instance.version          # like sys.version
    instance.version_info     # like sys.version_info
    instance.hexversion       # like sys.hexversion
    instance.vimversion       # version of vim editor, integer

    instance.name             # name of buffer in vim
    instance.text             # unicode object which contain buffer contents
    instance.newlines         # EOL string (may be '\\r', '\\n', or '\\r\\n')
    instance.encoding         # buffer encoding (vim variable &encoding)
    instance.buffer           # vim.buffer object assotiated with instance

    instance.closed           # False (file attribute)
    instance.mode             # 'rb+' (file attribute)

    instance.exceptions.BreakDialog  # built in excepton using for handle
                                     # Cancel button in replace_i() method
    """

    version      = VERSION
    version_info = VERSION_INFO
    hexversion   = HEXVERSION
    vimversion   = VIMVERSION

    ## }}}
    ## __init__ and synchronization methods {{{2 100 fixed

    name     = None
    text     = u""
    newlines = None
    encoding = None
    buffer   = None
    exceptions = _ExceptionsContainer()

    def __init__(self, buffer=vim.current.buffer):
        self.update_vi2py(buffer)
        self.re = _RegExp(self)
        self.name = self.buffer.name

    def update_vi2py(self, buffer=vim.current.buffer):
        """\
        update_vi2py([buffer]) -> None

        Read information from vim buffer and update some object data:
        self.text, self.buffer, self.newlines and self.encoding. (See class
        documentation for meaning of this data).
        This metod using, for example, in class constractor.
        <synchronization-methods>
        """

        try:
            vim.command("b %i"%buffer.number)
        except AttributeError:
            try:
                vim.command("b %s"%buffer.name)
            except: pass
        newlines = vim.eval("&fileformat")
        newlines = {"dos" :"\r\n",
                    "unix":"\n",
                    "mac" :"\r"}[newlines]
        encoding = re.sub(r"^(?:8bit|2byte)-","",vim.eval("&encoding"))
        try: u"".encode(encoding)
        except LookupError:
            try:
                encoding = {
                    "ucs-2"   : "utf-8",            # FIXME is it right?
                    "ucs-2le" : "unicode-internal"  # FIXME is it right?
                    }[encoding]
                _print_warning(re.sub("(?m)^", " |  ",
                    "Warning: I have selected python codec '%s'\n"\
                    "but I don't know am I right. Report me about problems.\n"
                    "    Note: script version is:\n%s"%(encoding,
                            re.sub(
                                "(?m)^", r">>> ", self.version
                                ))))
            except KyeError:
                raise LookupError(re.sub("(?m)^", " |  ",
                    "\ntext.py module not provided encoding scheme '%s'\n"\
                    "to avoid this problem there are two ways:\n"\
                    "1) may be python know this encoding under another name\n"\
                    "2) if not, we can create any encoding ourselves.\n"\
                    "Please report to maintainer about this bug.\n"\
                    "    Note: script version is:\n%s"%(encoding,
                        re.sub(
                            "(?m)^", r">>> ", self.version
                            ))))
        self.text     = newlines.join(buffer)
        self.buffer   = buffer
        self.newlines = newlines
        self.encoding = encoding

    def update_py2vi(self):
        """\
        update_py2vi() -> None

        write self.text into vim.buffer
        <synchronization-methods>
        """

        self.buffer[:] = self.text.split(self.newlines)

    ## }}}
    ## offset methods {{{2

    def offset2LC(self, offset):
        """\
        offset2LC(offset) -> tuple

        Get offset in python notation (zero-leader) and return pair (line,
        column) in vim notation: (1-leader).
        <offset-methods>
        """

        line   =          int(vim.eval("byte2line(%i)"%(offset+1)))
        column = offset - int(vim.eval("line2byte(%i)"%line)) + 2
        return line, column

    def LC2offset(self, line, column):
        """\
        LC2offset(line, column) -> int

        Get pair (line, column) in vim notation: (1-leader) and return offset
        in python notation (zero-leader).
        <offset-methods>
        """

        line = int(vim.eval("line2byte(%i)"%line))
        return line + column

    ## }}}
    ## string-like and sequence-like methods {{{2
    ## slice operation {{{3

    def __setitem__(self, key, value):
        """\
        Supporting set slice operation: Text_object[a:b]='string'
        <sequence-methods>
        """
        # type test
        if not isinstance(value, basestring):
            raise TypeError("__setitem__ method mast take a string")
        if isinstance(key, int):
            # convert key to slice object (empty teakettle :) )
            if key <  0: key += len(self)
            if key >= len(self) or key < 0:
                raise IndexError
            key = slice(key,key+1)
        # convert slice to two integers
        try:
            start = key.start or 0
            stop  = key.stop  or {0:0, None:len(self)}[key.stop]
        except KeyError:
            raise TypeError
        if sys.hexversion < 0x2020000 and stop == sys.maxint:   # python 2.1
            stop = len(self)
        if start < 0: start += len(self)
        if stop  < 0: stop  += len(self)
        start = max(start, 0)
        stop  = max(stop, 0)
        # apply step argument
        if key.step:
            value = value.replace("\r\n","\n")
            value = list(unicode(value, self.encoding))[::key.step]
            value = "".join(value).encode(self.encode)
        # encode value if necesary
        if isinstance(value, unicode):
            value=value.encode(self.encoding)
        # get vim buffer address and contents
        line_b, col_b = self.offset2LC(start)
        line_e, col_e = self.offset2LC(stop)
        line_content  = vim.eval("getline(%i)"%line_b)
        left  = line_content[:col_b-1]
        if line_b < line_e:
            line_content = vim.eval("getline(%i)"%line_e)
        elif line_b > line_e:
            raise re.sub("(?m)^", " |  ",
                    "\nThis should not be\n"\
                    "Please report to maintainer about this bug.\n"\
                    "    Note: script version is:\n%s"%re.sub(
                            r"(?m)^", ">>> ", self.version
                            ))
        right = line_content[col_e-1:]
        # change internal representation
        self.text = self.text[:start]+value+self.text[stop:]
        # prepare value for vim buffer
        value = left + value + right
        value = re.split(r"\r\n?|\n", value)    # because newlines may be
                                                # different, we using regexp
        # change vim buffer
        self.buffer[line_b-1:line_e] = value

    def __delitem__(self, key):
        """\
        Supporting del slice operation: del(Text_object[a:b])
        <sequence-methods>
        """
        self[key] = ""

    def __getitem__(self, key):
        """\
        Supporting get slice operation: variable = Text_object[a:b]
        <sequence-methods>
        """
        return self.text.__getitem__(key)

    if sys.hexversion < 0x2030000:              # for python 2.2
        def __getslice__(self, *key):
            return self.text.__getslice__(*key)
        def __setslice__(self, start, stop, value):
            return self.__setitem__(slice(start,stop), value)
        def __delslice__(self, start, stop):
            return self.__delitem__(slice(start,stop))

    ## }}}
    ## sequence-service {{{3

    def __len__(self):
        """\
        Supporting len() function: len(Text_object) -> int
        <sequence-methods>
        """
        return len(self.text)

    def __contains__(self, item):
        """\
        Supporting membership test: 'string' in Text_object -> bool
        <sequence-methods>
        """
        return self.text.__contains__(item)

    def __iadd__(self, other):
        """\
        Supporting  += operator:
        Text_object += 'string' -> None # append the string to the buffer
        Text_object += list     -> None # append list of string line by line
        <sequence-methods>
        """

        len_s = len(self)
        self[len_s:len_s] = other

    def append(self, other):
        """\
        append(string) -> None

        append STRING to the end of buffer
        <sequence-methods>
        """
        self += other

    def extend(self, other):
        """\
        extend(list) -> None

        append LIST of strings to the end of buffer
        <sequence-methods>
        """
        self += other

    def __imul__(self, other):
        """\
        Supporting  *= operator:
        Text_object *= 0   -> None # delete buffer contains
        Text_object *= 1   -> None # nothing todo
        Text_object *= Int -> None # duplicate buffer contains
                                   # as mach as needed
        <sequence-methods>
        """

        if other==0:
            self.buffer[:]=""
            self.update_vi2py()
        else:
            save = self.text
            for i in xrange(other-1): self.append(save)

    def insert(self, index, other):
        """\
        insert(index, other) -> None

        Insert OTHER in INDEX position (same as self[INDEX:INDEX] = OTHER)
        <sequence-methods>
        """
        self[index:index] = other

    def remove(self, item):
        """\
        remove(item) -> None

        Same as del self[self.index(item)]
        <sequence-methods>
        """
        del self[self.index(item)]

    def reverse(self, how="strings"):
        """\
        reverse([how]) -> None

        Reverse buffer. If HOW is 'strings' (this is default) reverse string
        order if 'letters', reverse letters order.
        <sequence-methods>
        """
        if   how == 'strings':
            l = list(self.buffer)
            l.reverse()
            self[:] = self.newlines.join(l)
        elif how == 'letters':
            l = list(re.sub(ur"\r\n?",ur"\n",unicode(self.text,self.encoding)))
            l.reverse()
            self[:] = "".join(l).encode(self.encoding).replace("\n",self.newlines)
        else:
            raise TypeError("Bad argument %r in reverse method. "\
                    "Must be 'strings' or 'letters'"%how)

    ## TODO: pop(), sort()

    ## }}}
    ## representation {{{3

    def __str__(self):
        "Support str() function"
        return self.text.__str__()

    ## }}}
    ## information methods (not change buffer) {{{3

    def count (self, item, *pos):
        """\
        count( sub[, start[, end]]) -> int

        Return the number of occurrences of substring SUB in buffer[start:end].
        Optional arguments START and END are interpreted as in slice
        notation.
        <string-methods>
        """

        if isinstance(item, unicode):
            item = item.encode(self.encoding)
        return self.text.count (item, *pos)

    def index (self, item, *pos):
        """\
        index( sub[, start[, end]]) -> int

        Like find(), but raise ValueError when the substring is not found.
        <string-methods>
        """

        if isinstance(item, unicode):
            item = item.encode(self.encoding)
        return self.text.index (item, *pos)

    def find  (self, item, *pos):
        """\
        find( sub[, start[, end]]) -> int

        Return the lowest index in the buffer where substring SUB is found,
        such that SUB is contained in the range (START, END). Optional
        arguments START and END are interpreted as in slice notation. Return -1
        if sub is not found. 
        <string-methods>
        """

        if isinstance(item, unicode):
            item = item.encode(self.encoding)
        return self.text.find  (item, *pos)

    def rindex(self, item, *pos):
        """\
        rindex( sub[, start[, end]]) -> int

        Like rfind() but raises ValueError when the substring SUB is not
        found.
        <string-methods>
        """

        if isinstance(item, unicode):
            item = item.encode(self.encoding)
        return self.text.rindex(item, *pos)

    def rfind (self, item, *pos):
        """\
        rfind( sub [,start [,end]]) -> int

        Return the highest index in the buffer where substring SUB is found,
        such that SUB is contained within range (START, END). Optional
        arguments START and END are interpreted as in slice notation. Return -1
        on failure. 
        <string-methods>
        """

        if isinstance(item, unicode):
            item = item.encode(self.encoding)
        return self.text.rfind (item, *pos)

    def endswith(self, suffix, *pos):
        """\
        endswith( suffix[, start[, end]]) -> int

        Return True if the buffer ends with the specified SUFFIX, otherwise
        return False. With optional START, test beginning at that position.
        With optional END, stop comparing at that position.
        <string-methods>
        """

        if isinstance(suffix, unicode):
            suffix = suffix.encode(self.encoding)
        return self.text.endswith(suffix, *pos)

    def statswith(self, prefix, *pos):
        """\
        startswith( prefix[, start[, end]]) -> int

        Return True if the buffer starts with the PREFIX, otherwise return
        False.  With optional START, test string beginning at that position.
        With optional END, stop comparing string at that position.
        <string-methods>
        """

        if isinstance(prefix, unicode):
            prefix = prefix.encode(self.encoding)
        return self.text.statswith(prefix, *pos)

    def isalnum(self):
        """\
        isalnum() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).isalnum()

    def isalpha(self):
        """\
        isalpha() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).isalpha()

    def isdigit(self):
        """\
        isdigit() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).isdigit()

    def islower(self):
        """\
        islower() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).islower()

    def isspace(self):
        """\
        isspace() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).isspace()

    def istitle(self):
        """\
        istitle() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).istitle()

    def isupper(self):
        """\
        isupper() -> bool

        I think it is low usefull, but provide for string compatibility
        <string-methods>
        """

        return unicide(self.text, self.encoding).isupper()

    ## }}}
    ## changing lines methods {{{3

    def apply_to_lines(self, func, *pos):
        """\
        apply_to_lines(func [, line_number or , start, stop [, step]]) -> None

        apply FUNC to every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        NOTE:
        If you need to do some change to whole buffer (like convert all letters
        to upper case, for example) may be more swift is apply your FUNC to
        self.text and then call self.update_py2vi() method.
        <string-methods>
        """

        if   len(pos)==0: generator = xrange(len(self.buffer))
        elif len(pos)==1: generator = pos
        else:             generator = xrange(*pos)
        for i in generator:
            try: 
                self.buffer[i] = func(unicode(self.buffer[i],
                    self.encoding)).encode(self.encoding)
            except IndexError: break
        self.update_vi2py(self.buffer)

    def center(self, width, *pos):
        """\
        center(width [, line_number or , start, stop [, step]]) -> None

        cetnter every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.center(width), *pos)

    def rjust(self, width, *pos):
        """\
        rjust(width [, line_number or , start, stop [, step]]) -> None

        rjust every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.rjust(width), *pos)

    def ljust(self, width, *pos):
        """\
        ljust(width [, line_number or , start, stop [, step]]) -> None

        ljust every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.ljust(width), *pos)

    def zfill(self, width, *pos):
        """\
        zfill(width [, line_number or , start, stop [, step]]) -> None

        zfill every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.zfill(width), *pos)

    def rstrip(self, chars=None, *pos):
        """\
        rstrip([chars] [, line_number or , start, stop [, step]]) -> None

        rstrip every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.rstrip(chars), *pos)

    def lstrip(self, chars=None, *pos):
        """\
        lstrip([chars] [, line_number or , start, stop [, step]]) -> None

        lstrip every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.lstrip(chars), *pos)

    def strip(self, chars=None, *pos):
        """\
        strip([chars] [, line_number or , start, stop [, step]]) -> None

        strip every (default) lines in buffer or in line by LINE_NUMBER
        or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.strip(chars), *pos)

    def capitalize(self, *pos):
        """\
        capitalize([, line_number or , start, stop [, step]]) -> None

        capitalize case in every (default) lines in buffer or in line by 
        LINE_NUMBER or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x:
                unicode(x,self.encoding).capitalize().encode(self.encoding),
                *pos)

    def lower(self, *pos):
        """\
        lower([, line_number or , start, stop [, step]]) -> None

        lower case in every (default) lines in buffer or in line by
        LINE_NUMBER or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x:
                unicode(x,self.encoding).lower().encode(self.encoding),
                *pos)

    def swapcase(self, *pos):
        """\
        swapcase([, line_number or , start, stop [, step]]) -> None

        toggle case in every (default) lines in buffer or in line by
        LINE_NUMBER or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x:
                unicode(x,self.encoding).swapcase().encode(self.encoding),
                *pos)

    def title(self, *pos):
        """\
        title([, line_number or , start, stop [, step]]) -> None

        case like in title in every (default) lines in buffer or in line by
        LINE_NUMBER or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x:
                unicode(x,self.encoding).title().encode(self.encoding),
                *pos)

    def upper(self, *pos):
        """\
        upper([, line_number or , start, stop [, step]]) -> None

        upper case in every (default) lines in buffer or in line by 
        LINE_NUMBER or to lines in range from START to STOP by STEP.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x:
                unicode(x,self.encoding).upper().encode(self.encoding),
                *pos)

    def replace(self, old, new, maxsplit=None, *pos):
        """\
        replace(old, new [, maxsplit] [, line_number or , start, stop [, step]])
                -> None

        replace substring OLD to NEW in every (default) lines in buffer
        or in line by LINE_NUMBER or to lines in range from START to STOP
        by STEP. If MAXSPLIT is given, only first MAXSPLIT occurrences are
        replaced in every lines.

        See also NOTE in self.apply_to_lines() method
        <string-methods>
        """

        if isinstance(old, unicode): old.encode(self.encoding)
        if isinstance(new, unicode): new.encode(self.encoding)
        if isinstance(maxsplit, int):
            self.apply_to_lines(lambda x: x.replace(old,new,maxsplit), *pos)
        else:
            self.apply_to_lines(lambda x: x.replace(old,new), *pos)

    def expandtabs(self, tabsize=8, *pos):
        """\
        expandtabs([tabsize] [, line_number or , start, stop [, step]])
                -> None

        expandtabs in every (default) lines in buffer or in line by
        LINE_NUMBER or to lines in range from START to STOP by STEP.
        Default TABSIZE = 8.

        See also NOTES in self.apply_to_lines() method
        <string-methods>
        """

        self.apply_to_lines(lambda x: x.expandtabs(tabsize), *pos)

    ## }}}
    ## other string methods {{{3

    def decode(self, *args):
        """\
        decode([encoding [, errors]]) -> unicode_object

        Decodes the string using the codec registered for self.encoding. ERRORS
        may be given to set a different error handling scheme. The default is
        'strict', meaning that encoding errors raise ValueError. Other possible
        values are 'ignore' and replace'.
        <string-methods>
        """

        if   len(args) == 0: args = (self.encoding, 'strict')
        elif len(args) == 1: args = (args[0],       'strict')
        elif len(args) != 2:
            raise TypeError("decode() method take 2 optional arguments")
        return unicode(self.text,*args)

    def encode(self, *args):
        """\
        encode([encoding [, errors]]) -> string

        Return an encoded version of the string. This method may be use for
        convert from one encoging system into another.  Default encoding is
        self.encoding attribute. errors may be given to set a different error
        handling scheme. The default for errors is 'strict', meaning that
        encoding errors raise a ValueError. Other possible values are 'ignore'
        and 'replace'.
        <string-methods>
        """

        if   len(args) == 0: args = (self.encoding, 'strict')
        elif len(args) == 1: args = (args[0],       'strict')
        elif len(args) != 2:
            raise TypeError("encode() method take 2 optional arguments")
        return self.decode(*args).encode(*args)

    def split(self, *args):
        """\
        split( [sep [,maxsplit]]) -> list

        Return a list of the words in the buffer, using sep as the delimiter
        string. If maxsplit is given, at most maxsplit splits are done. If sep
        is not specified or None, any whitespace string is a separator.
        <string-methods>
        """

        return self.text.split(*args)

    def splitlines(self, *args):
        """\
        splitlines( [keepends]) -> list

        Return a list of the lines in the buffer, breaking at line boundaries.
        Line breaks are not included in the resulting list unless keepends is
        given and true. 
        <string-methods>
        """

        return self.text.splitlines(*args)

    ## }}}
    ## }}}
    ## file-like methods: {{{2

    def isatty(self):
        """\
        Always False
        <file-methods>
        """
        return False

    def close(self):
        """\
        Nothing to do, return None
        <file-methods>
        """
        pass

    def flush(self):
        """\
        Nothing to do, return None
        <file-methods>
        """
        pass
    
    closed = False
    mode = "rb+"

    def tell(self):
        """\
        tell() -> int

        return position in the file (byte offset)
        <file-methods>
        """

        line   = int(vim.eval("line('.')"))
        column = int(vim.eval("col('.')"))
        return self.LC2offset(line, column)

    def seek(self, offset, whence=0):
        """\
        seek(offset[, whence]) -> None

        Move to new file position. Argument offset is a byte count. Optional
        argument whence defaults to 0 (offset from start of file, offset should
        be >= 0);  other values are 1 (move relative to current position,
        positive or negative),  and 2 (move relative to end of file, negative)
        <file-methods>
        """

        if   whence == 0:
            vim.eval("cursor(%i,%i)"%self.offset2LC(offset))
        elif whence == 1:
            line   = int(vim.eval("line('.')"))
            column = int(vim.eval("col('.')"))
            current_offset = self.LC2offset(line, column)
            vim.eval("cursor(%i,%i)"%self.offset2LC(current_offset + offset))
        elif whence == 2:
            line   = int(vim.eval("line('$')"))
            column = int(vim.eval("col('$')"))
            vim.eval("cursor(%i,%i)"%self.offset2LC(len(self) - offset))
        else:
            raise TypeError("second argument seek() method must be 0, 1 or 2")

    def truncate(self, size=None):
        """\
        truncate([size]) -> None

        Truncate the buffer to at most size bytes. Size defaults to the current
        file position, as returned by tell().
        <file-methods>
        """

        if size==None: size=self.tell()
        del(self[size:])

    def read(self, size=-1):
        """\
        read([size]) -> string

        Read at most size bytes from the file. If the size argument is negative
        or omitted, read all data until end of buffer is reached.
        <file-methods>
        """

        pos=self.tell()
        if size >= 0:
            self.seek(size,1)
            return self[pos:pos+size]
        else:
            self.seek(0,2)
            return self[pos:]

    def readline(self, size=-1):
        """\
        readline([size]) -> string

        Read one entire line from the file. A trailing newline character is
        kept in the string. If the size argument is present and non-negative,
        it is a maximum byte count (including the trailing newline) and an
        incomplete line may be returned.
        <file-methods>
        """

        pos = self.tell()
        try:
            result = self[pos:self.index(self.newlines,pos)]+self.newlines
        except ValueError:
            result = self[pos:]
        if size >= 0:
            self.seek(pos+size,0)
            return result[:size]
        else:
            self.seek(pos+len(result))
            return result

    def readlines(self, sizehint=0):
        """\
        readlines([sizehint]) -> list

        Read until end of buffer using readline() and return a list containing
        the lines thus read. If the optional sizehint argument is present,
        instead of reading up to end of buffer, whole lines totalling
        approximately sizehint bytes are read.
        <file-methods>
        """

        total = 0
        lines = []
        line  = self.readline()
        while line:
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines

    def write(self, string):
        """\
        write(str) -> None

        Write a string to the buffer under coursor.
        There is no return value.
        <file-methods>
        """

        if isinstance(string, unicode):
            string = string.encode(self.encoding)
        pos = self.tell()
        string = re.sub(r"\r\n?|\n",self.newlines,string)
        self[pos:pos] = string
        self.seek(pos+len(string))

    def writelines(self, list):
        """\
        writelines(list) -> None

        Write a sequence of strings to the file. The sequence can be any
        iterable object producing strings, typically a list of strings. There
        is no return value. (The name is intended to match readlines();
        writelines() does not add line separators.)
        <file-methods>
        """

        self.write(''.join(list))

    ## }}}
    ## Interactive {{{2

    def interactive(self, start=None, end=None, *confirm, **options):
        """\
        interactive([start [, end [, msg [, choices [, default [, type]]]]]
                    [, highlight=group] [, vpos="bot" (or "top")]
                    [, gap=gap]]) -> int

        Go to START position, hilight from START to END by GROUP (default = 
        "IncSearch"), and run vim's confirmation dialog. By default START
        and END setups to current position (tell() method). Arguments MSG,
        CHOICES, DEFAULT and TYPE pass into vim's confirm() function.
        MSG = "request" by default. See ":help confirm()" in vim editor for
        details. VPOS may be "top" or "bot" (deafult) --- were in window
        show the highlighted text. GAP is number of lines between top border
        of window and highlighted text if VPOS="top" or between bottom border
        of window and highlighted text. By default GAP == 3.
        Return number of choice (start from 1) or 0.
        <interactive-methods>
        """

        ## inits
        if not _IS_DIALOG_ENABLED:
            raise "Dialog not availabel: vim has not necessary feature"

        ## defaults
        if start == None: start   = self.tell()
        if end   == None: end     = self.tell()
        if not confirm:   confirm = ("request",)
        if not options.has_key("highlight"): options["highlight"] = "IncSearch"
        if not options.has_key("vpos"):      options["vpos"]      = "bot"
        if not options.has_key("gap"):       options["gap"]       = 3

        ## compute position
        (start_l, start_c) = self.offset2LC(start)
        (end_l,   end_c)   = self.offset2LC(end)

        ## redraw
        if   options["vpos"] == "top":
            vim.command("normal! %izt"%(max(start_l-options["gap"], 1)))
        elif options["vpos"] == "bot":
            vim.command("normal! %izb"%(min(end_l+options["gap"],
                int(vim.eval("line('$')")))))
        vim.command("match %s /\\%%%il\\%%%ic\\_.*\\%%%il\\%%%ic/"%(
            options["highlight"], start_l, start_c, end_l, end_c))
        vim.command("redraw")

        ## confirmation
        def advanced_str(obj):
            if isinstance(obj, unicode):
                if "c" in vim.eval("&guioptions"):
                    dialog_encoding = self.encoding
                else:
                    dialog_encoding = locale.getdefaultlocale()[1]
                return obj.encode(dialog_encoding)
            else:
                return str(obj)
        confirm = map(advanced_str, confirm)
        result  = vim.eval("confirm(%s)"%("'"+"', '".join(confirm)+"'"))
        vim.command("match None /\\%%%il\\%%%ic\\_.*\\%%%il\\%%%ic/"%(
            start_l, start_c, end_l, end_c))
        return int(result)

    def replace_i(self, start=None, end=None, 
            rep_list=[], msg="Choose one for substitution", **options):
        """\
        replace_i([start [, end [, repl_list [, msg]]]]
                  [, highlight=group] [, vpos="bot" (or "top")]
                  [, gap=gap] [, buttons = YES|NO|CANCEL]]) -> bool or raise

        REPL_LIST is any sequence of replacements (list of strings, for
        example). BUTTONS is list of button displayed in the dialog. It may be
        bitwise summ of following constanses: YES, NO, OTHER, CANCEL, BREAK.
        Default is YES|NO|CANCEL. Other arguments meaning same as in
        interactive() method. Return False if replace rejected, True otherwise.
        Raise CancelDialog if Cancel button selected. Raise BreakDialog if
        Break button selected. Raise OtherDialog if Other button selected
        <interactive-methods>
        """

        ## inits
        if not _IS_DIALOG_ENABLED:
            raise "Dialog not availabel: vim has not necessary feature"

        ## making default
        if not options.has_key("buttons"): options["buttons"] = YES|NO|CANCEL

        ## compouse button range
        choices = ""
        for i,j in enumerate(rep_list):
            j = re.sub(r"\r\n?|\n","\xff", j)
            if len(j)> max(len(msg), 20):
                j = j[:max(len(msg), 20)-3] + "..."
            if i<10: choices = choices + "\n&%i: %s"%(i,j)
            else:    choices = choices + "\n%i: %s"%(i,j)
        choices = choices.lstrip()
        if options["buttons"] & YES:    choices = choices + "\n&Yes"
        if options["buttons"] & NO:     choices = choices + "\n&No"
        if options["buttons"] & OTHER:  choices = choices + "\n&Other"
        if options["buttons"] & CANCEL: choices = choices + "\n&Cancel"
        if options["buttons"] & BREAK:  choices = choices + "\n&Break"

        ## make request
        choice = self.interactive(start, end,
                msg, choices, 1, "Question", **options)

        ## apply result of request
        if not choice:
            return False
        elif choice <= len(rep_list):
            self[start:end] = rep_list[choice-1]
            return True
        else:
            choice = re.search(r"(?:.*\n){%i}&?(.*)"%(choice-1),choices).group(1)
            if   choice == "Yes": self[start:end] = rep_list[0]; return True
            elif choice == "No":     return False
            elif choice == "Other":  raise  OtherDialog
            elif choice == "Cancel": raise  CancelDialog
            elif choice == "Break":  raise  BreakDialog

    ## }}}
## }}}

## vim: et:ro:sw=4:fdm=marker:ts=8
