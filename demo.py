import xml.etree.cElementTree as ET
from xml.etree.cElementTree import XMLParser
from xml.etree.ElementTree import TreeBuilder, Element


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


@register('log')
class LogElement(FunctionElement):
    def do(self):
        print 'log>', self.text


@register('testsuite')
class TestSuiteElement(FunctionElement):
    def do(self):
        name = self.attrib.get('name')
        if name:
            print 'testsuite>', name


@register('if')
class IfElement(FunctionElement):
    def run(self):
        condition = self.attrib.get('condition')
        if bool(condition):
            super(IfElement, self).run()


def _element_factory(tag, attrs):
    cls = __function_table__.get(tag.lower(), FunctionElement)
    return cls(tag, attrs)


_parser = XMLParser(target=TreeBuilder(_element_factory))
tree = ET.parse('demo.xml', parser=_parser)
root = tree.getroot()

root.run()