from __future__ import unicode_literals

from .writers import Writer
from .html_paths import HtmlPath, HtmlPathElement


class _Element(object):
    #:: Self, str, dict[str, str] | none -> none
    def __init__(self, name, attributes):
        if attributes is None:
            #:: dict[str, str]
            attributes = {}
        
        self.name = name
        self.attributes = attributes
        self.written = False


class HtmlGenerator(object):
    #:: Self, (-> Writer) -> none
    def __init__(self, create_writer):
        #:: list[_Element]
        self._stack = []
        self._create_writer = create_writer
        self._writer = create_writer()
    
    #:: Self, str -> none
    def text(self, text):
        if text:
            self._write_all()
            self._writer.text(text)
    
    #:: Self, str, ?attributes: dict[str, str], ?always_write: bool -> none
    def start(self, name, attributes=None, always_write=None):
        self._stack.append(_Element(name, attributes))
        
        if always_write:
            self._write_all()

    #:: Self -> none
    def end(self):
        element = self._stack.pop()
        if element.written:
            self._writer.end(element.name)
    
    #:: Self -> none
    def end_all(self):
        while self._stack:
            self.end()
    
    #:: Self, str, ?attributes: dict[str, str] -> none
    def self_closing(self, name, attributes=None):
        self._writer.self_closing(name, attributes)
    
    #:: Self -> none
    def _write_all(self):
        for element in self._stack:
            if not element.written:
                element.written = True
                self._write_element(element)
    
    #:: Self, _Element -> none
    def _write_element(self, element):
        self._writer.start(element.name, element.attributes)
    
    #:: Self, HtmlGenerator -> none
    def append(self, other):
        other_string = other.as_string()
        if other_string:
            self._write_all()
            self._writer.append(other_string)
    
    #:: Self -> str
    def as_string(self):
        return self._writer.as_string()
    
    #:: Self -> HtmlGenerator
    def child(self):
        return HtmlGenerator(self._create_writer)


#:: HtmlGenerator, HtmlPath -> none
def satisfy_html_path(generator, path):
    first_unsatisfied_index = _find_first_unsatisfied_index(generator, path)
    while len(generator._stack) > first_unsatisfied_index:
        generator.end()
    
    for element in path.elements[first_unsatisfied_index:]:
        #:: dict[str, str]
        attributes = {}
        if element.class_names:
            attributes["class"] = _generate_class_attribute(element)
        generator.start(element.names[0], attributes=attributes)
    

#:: HtmlGenerator, HtmlPath -> int
def _find_first_unsatisfied_index(generator, path):
    for index, (generated_element, path_element) in enumerate(zip(generator._stack, path.elements)):
        if not _is_element_match(generated_element, path_element):
            return index
    
    return len(generator._stack)


#:: _Element, HtmlPathElement -> bool
def _is_element_match(generated_element, path_element):
    return (
        not path_element.fresh and
        generated_element.name in path_element.names and
        generated_element.attributes.get("class", "") == _generate_class_attribute(path_element)
    )


#:: HtmlPathElement -> str
def _generate_class_attribute(path_element):
    return " ".join(path_element.class_names)
