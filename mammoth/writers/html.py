# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from .abc import Writer

import cgi


class HtmlWriter(Writer):
    # do this the old fashioned way for 2.x. 3.x, we could make a table...
    # for more characters, see https://www.utexas.edu/learn/html/spchar.html

    WORD2ASCII =  {   #             // www.fileformat.info/info/unicode/<NUM>/ <NUM> = 2018
        u'\u00AB':u'<<',     # « (U+00AB) in UTF-8
        u'\u00BB':u'>>',     # » (U+00BB) in UTF-8
        u'\u2018':u"'",      # ‘ (U+2018) in UTF-8
        u'\u2019':u"'",      # ’ (U+2019) in UTF-8
        u'\u201A':u"'",      # ‚ (U+201A) in UTF-8
        u'\u201B':u"'",      # ‛ (U+201B) in UTF-8
        u'\u201C':u"\"",      # “ (U+201C) in UTF-8
        u'\u201D':u"\"",      # ” (U+201D) in UTF-8
        u'\u201E':u"\"",      # „ (U+201E) in UTF-8
        u'\u201F':u"\"",      # ‟ (U+201F) in UTF-8
        u'\u2039':u"<",      # ‹ (U+2039) in UTF-8
        u'\u203A':u">",      # (U+203A) in UTF-8
        u'\u2013':u"-",      # – (U+2013) in UTF-8
        u'\u2014':u"--",     # — (U+2014) in UTF-8
        u'\u2026':u"...",     # … (U+2026) in UTF-8
        u'\u00A9':u"(c)",      # (c) U+00a9 in UTF-8
        u'\u00B5':u"u"
    }

    WORD2HTML =  {   #             // www.fileformat.info/info/unicode/<NUM>/ <NUM> = 2018
        u'\u00AB':u'&laquo;',     # « (U+00AB) in UTF-8
        u'\u00BB':u'&raquo;',     # » (U+00BB) in UTF-8
        u'\u2018':u"'",      # ‘ (U+2018) in UTF-8
        u'\u2019':u"'",      # ’ (U+2019) in UTF-8
        u'\u201A':u"'",      # ‚ (U+201A) in UTF-8
        u'\u201B':u"'",      # ‛ (U+201B) in UTF-8
        u'\u201C':u"\"",      # “ (U+201C) in UTF-8
        u'\u201D':u"\"",      # ” (U+201D) in UTF-8
        u'\u201E':u"\"",      # „ (U+201E) in UTF-8
        u'\u201F':u"\"",      # ‟ (U+201F) in UTF-8
        u'\u2039':u"<",      # ‹ (U+2039) in UTF-8
        u'\u203A':u">",      # (U+203A) in UTF-8
        u'\u2013':u"&ndash;",      # – (U+2013) in UTF-8
        u'\u2014':u"&mdash;",     # — (U+2014) in UTF-8
        u'\u2026':u"...",     # … (U+2026) in UTF-8
        u'\u00A9':u"&copy;",
        u'\u00B5':u"&micro;"
    }

    def __init__(self, output_args=None):

        self._conversion_set = None
        if output_args == 'ascii':
            self._conversion_set = HtmlWriter.WORD2ASCII
        if output_args == 'html':
            self._conversion_set = HtmlWriter.WORD2HTML

        self._fragments = []


    def translate_word_text(self, text):
        for key, value in self._conversion_set.iteritems():
            text = text.replace(key, value)
        return text

    def text(self, text):
        text = _escape_html(text)
        if self._conversion_set != None:
            text = self.translate_word_text(text)

        self._fragments.append(text)
    
    def start(self, name, attributes=None):
        attribute_string = _generate_attribute_string(attributes)
        self._fragments.append("<{0}{1}>".format(name, attribute_string))

    def end(self, name):
        self._fragments.append("</{0}>".format(name))
    
    def self_closing(self, name, attributes=None):
        attribute_string = _generate_attribute_string(attributes)
        self._fragments.append("<{0}{1} />".format(name, attribute_string))
    
    def append(self, html):
        self._fragments.append(html)
    
    def as_string(self):
        return "".join(self._fragments)

    @classmethod
    def validate_options(cls, options):
        return options in ["ascii", "html"]

def _escape_html(text):
    return cgi.escape(text, quote=True)


def _generate_attribute_string(attributes):
    if attributes is None:
        return ""
    else:
        return "".join(
            ' {0}="{1}"'.format(key, _escape_html(attributes[key]))
            for key in sorted(attributes)
        )
