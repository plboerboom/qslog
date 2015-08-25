from qslog import transition

def onenterhome(e):
    e.command.prompt = '> '
    
def onenterone(e):
    print e.command.line
    e.command.prompt = 'one: '

@transition
def do_wo(self, line):
    self.line = line

@transition
def do_abort(self, line):
    pass

def onentertwo(e):
    e.command.prompt = 'two: '

@transition
def do_two(self, line):
    pass

@transition
def do_home(self, line):
    pass


state_config = {
        'initial': {'state': 'home', 'defer': True},
        'events': [
            {'name': 'wo', 'src' : 'home', 'dst' : 'one'},
            {'name': 'abort', 'src': 'one', 'dst': 'home'},
            {'name': 'two', 'src' : 'one', 'dst': 'two'},
            {'name': 'two', 'src': 'two', 'dst': 'two'},
            {'name': 'home', 'src': 'two', 'dst': 'home'}
            ]
        }

# TODO: Figure out how to pass state across transitions
# TODO: Write data
# TODO: Autocomplete
# TODO: Control state transition with logic in command
