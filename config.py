from qslog import transition

def onstartup(e):
    print 'starting up'

def onenterhome(e):
    e.command.prompt = 'home: '
    
def onenterone(e):
    e.command.prompt = 'one: '

@transition
def do_goto_one(self, line):
    print line

@transition
def do_abort(self, line):
    pass

def onentertwo(e):
    e.command.prompt = 'two: '

@transition
def do_goto_two(self, line):
    pass

@transition
def do_goto_home(self, line):
    pass


state_config = {
        'initial': {'state': 'home', 'defer': True},
        'events': [
            {'name': 'goto_one', 'src' : 'home', 'dst' : 'one'},
            {'name': 'abort', 'src': 'one', 'dst': 'home'},
            {'name': 'goto_two', 'src' : 'one', 'dst': 'two'},
            {'name': 'goto_two', 'src': 'two', 'dst': 'two'},
            {'name': 'goto_home', 'src': 'two', 'dst': 'home'}
            ],
        }

# TODO: modify fysom to search for handlers in this module
#       rather than requiring explicit call-back registration
