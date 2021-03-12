import pluggy

hookspec = pluggy.HookspecMarker("byytest")
hookimpl = pluggy.HookimplMarker("byytest")

@hookspec
def add_options(parser):
    pass

@hookspec
def configure(options, config):
    pass

@hookspec
def beforeTest(test):
    pass

@hookspec
def afterTest(test, result):
    pass

@hookspec
def beforeResult(result):
    pass

@hookspec
def afterResult(result):
    pass

@hookspec
def end(result):
    pass