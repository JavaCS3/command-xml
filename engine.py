import xml.etree.cElementTree as ET
from xml.etree.ElementTree import TreeBuilder, Element
from xml.etree.cElementTree import XMLParser


class FunctionTag(Element):
    def __init__(self, tag, attrib, **extra):
        super(FunctionTag, self).__init__(tag, attrib, **extra)
        self.output_stack = [None]
        self.initialize()

    def initialize(self):
        pass

    def append(self, element):
        super(FunctionTag, self).append(element)
        element.output_stack = self.output_stack

    def last_output(self):
        return self.output_stack[-1]

    def do(self):
        pass

    def run(self):
        output = self.do()
        if output is not None:
            self.output_stack.append(output)  # record each non-none output
        for child in self:
            child.run()

    def __repr__(self):
        return '<%s %s at 0x%x>' % (type(self).__name__, repr(self.tag), id(self))


__function_table__ = {}


def register(name):
    def _wrapper(func):
        __function_table__[name] = func
        return func

    return _wrapper


def _element_factory(tag, attrs):
    cls = __function_table__.get(tag.lower(), FunctionTag)
    return cls(tag, attrs)


__parser = XMLParser(target=TreeBuilder(_element_factory))


def parse(source):
    return ET.parse(source, parser=__parser)
