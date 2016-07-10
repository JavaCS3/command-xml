import xml.etree.cElementTree as ET
from xml.etree.cElementTree import XMLParser
from xml.etree.ElementTree import TreeBuilder, Element


class FunctionTable(object):
    def function(self, name):
        func = getattr(self, 'func_' + name.lower(), None)
        if not callable(func):
            return None
        return func

    def func_testsuite(self, _, **kwargs):
        name = kwargs.get('name')
        if name:
            print name

    def func_sum(self, _,**kwargs):
        total = 0
        for k in kwargs:
            v = kwargs.get(k)
            if v:
                total += int(v)
        print 'sum=', total

    def func_log(self, data,**kwargs):
        print 'log:', data


class FunctionElement(Element):
    __function_table__ = FunctionTable()

    def __init__(self, tag, attrib={}, **extra):
        super(FunctionElement, self).__init__(tag, attrib, **extra)

    def run(self):
        func = self.__function_table__.function(self.tag)
        if func:
            func(self.text, **self.attrib)

    def __repr__(self):
        return '<%s %s at 0x%x>' % (type(self).__name__, repr(self.tag), id(self))


_parser = XMLParser(target=TreeBuilder(FunctionElement))
tree = ET.parse('demo.xml', parser=_parser)
root = tree.getroot()

def run(node):
    node.run()
    for child in node:
        run(child)

run(root)