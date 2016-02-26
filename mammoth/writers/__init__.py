from .html import HtmlWriter
from .markdown import MarkdownWriter


def writer(output_format=None, output_options=None):
    if output_format is None:
        output_format = "html"
    
    return _writers[output_format](output_options)

def validate_writer_options(output_format=None, output_options=None):
    if output_format is None:
        output_format = "html"

    return _writers[output_format].validate_options(output_options)

def formats():
    return _writers.keys()


_writers = {
    "html": HtmlWriter,
    "markdown": MarkdownWriter,
}
