import xml.etree.cElementTree as ET
from xml.etree.ElementTree import TreeBuilder, Element
from xml.etree.cElementTree import XMLParser


class FunctionElement(Element):
    def do(self):
        pass

    def run(self):
        self.do()
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
    cls = __function_table__.get(tag.lower(), FunctionElement)
    return cls(tag, attrs)


__parser = XMLParser(target=TreeBuilder(_element_factory))


def parse(source):
    return ET.parse(source, parser=__parser)
