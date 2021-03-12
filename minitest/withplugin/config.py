import sys
import argparse
import pluggy
import hooks
import plugin1
import plugin2


class Config(object):
    def __init__(self):
        self.pm = pluggy.PluginManager('byytest')
        self.pm.add_hookspecs(hooks)
        self.pm.register(self, 'config')
        self.loadPlugins([plugin1, plugin2])

        self.plugins = self.pm.hook
        self.parser = argparse.ArgumentParser('PROGRAM')
        
    def loadPlugins(self, plugins):
        for plugin in plugins:
            self.pm.register(plugin)

    def config(self, args):
        self.plugins.add_options(parser=self.parser)
        self.options = self.parser.parse_args(args)
        # print(self.options)
        self.plugins.configure(options=self.options, config=self)
    
    @hooks.hookimpl
    def add_options(self, parser):
        parser.add_argument('file_name', help='test module name')
        parser.add_argument('-v', '--version', action='store_true', help='show version')
        parser.add_argument('--plugin', action='store_true', help='show plugins')

    @hooks.hookimpl
    def configure(self, options, config):
        if options.plugin:
            for k,v in config.plugins.__dict__.items():
                print(k,v._nonwrappers)
            sys.exit(0)
        
        if options.version:
            print('Version: beta')
            sys.exit(0)

    