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
        self.inherit_env = False
        self.name = self.attrib.get('name', 'N/A')

    def do(self):
        print 'test case>', self.name

    def run(self):
        try:
            super(TestCaseTag, self).run()
        except Exception, e:
            print e
            print '!!! test case>', self.name, 'failed'


@register('echo')
class EchoTag(FunctionTag):
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

@register('eval')
class EvalTag(FunctionTag):
    def do(self):
        print eval(self.text, self.env)


@register('script')
class ScriptTag(FunctionTag):
    def do(self):
        exec self.text in self.env