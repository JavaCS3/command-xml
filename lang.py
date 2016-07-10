from engine import register, FunctionElement


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