from engine import register, FunctionTag


@register('log')
class LogTag(FunctionTag):
    def do(self):
        print 'log>', self.text


@register('testsuite')
class TestSuiteTag(FunctionTag):
    def do(self):
        name = self.attrib.get('name')
        if name:
            print 'test suite>', name


@register('testcase')
class TestCaseTag(FunctionTag):
    def initialize(self):
        self.name = self.attrib.get('name', 'N/A')

    def do(self):
        print 'test case>', self.name

    def run(self):
        try:
            super(TestCaseTag, self).run()
        except:
            print '!!!test case', self.name, 'failed'


@register('string')
class StringTag(FunctionTag):
    def do(self):
        return self.text


@register('expect')
class ExpectTag(FunctionTag):
    def do(self):
        if self.last_output() == self.text:
            print 'expect>', self.text
        else:
            raise Exception('Expect Failed')


@register('if')
class IfTag(FunctionTag):
    def run(self):
        condition = self.attrib.get('condition')
        if bool(condition):
            super(IfTag, self).run()
