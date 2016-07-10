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
            print 'test suite>', name


@register('testcase')
class TestCaseElement(FunctionElement):
    def initialize(self):
        self.name = self.attrib.get('name', 'N/A')

    def do(self):
        print 'test case>', self.name

    def run(self):
        try:
            super(TestCaseElement, self).run()
        except:
            print '!!!test case', self.name, 'failed'


@register('string')
class StringElement(FunctionElement):
    def do(self):
        return self.text


@register('expect')
class ExpectElement(FunctionElement):
    def do(self):
        if self.last_output() == self.text:
            print 'expect>', self.text
        else:
            raise Exception('Expect Failed')


@register('if')
class IfElement(FunctionElement):
    def run(self):
        condition = self.attrib.get('condition')
        if bool(condition):
            super(IfElement, self).run()
