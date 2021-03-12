from hooks import hookimpl


@hookimpl
def add_options(parser):
    group = parser.add_argument_group('group2', 'group1 description')
    group.add_argument('--summary', dest='plugin2_summary', help='test true')

@hookimpl
def configure(options, config):
    config.pm.register(Formater())


class Formater(object):
    @hookimpl
    def end(self):
        print('this invoke after all test finished')

    @hookimpl
    def beforeTest(self, test):
        print('='*80)
        print(f'run: {test._testMethodName}')
        print(f'doc: {test.getDescription()}')

    @hookimpl
    def afterTest(self, test, result):
        print('-'*20)
        print(f'= RESULT: {result} =')
        print('-'*20)
    