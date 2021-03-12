from hooks import hookimpl


@hookimpl
def add_options(parser):
    group = parser.add_argument_group('group1', 'group1 description')
    group.add_argument('--filter', help='test true')

@hookimpl
def configure(options, config):
    if options.filter is not None:
        config.pm.register(Plugin1())


class Plugin1(object):
    @hookimpl
    def afterCollect(self, suite):
        print('this invoke after suite collected')