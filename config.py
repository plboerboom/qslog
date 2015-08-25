from qslog import transition

def onstartup(e):
    pass

def onenterhome(e):
    e.command.prompt = 'home: '
    
def onenterone(e):
    e.command.prompt = 'one: '

@transition
def do_one(self, line):
    pass

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
            {'name': 'one', 'src' : 'home', 'dst' : 'one'},
            {'name': 'abort', 'src': 'one', 'dst': 'home'},
            {'name': 'two', 'src' : 'one', 'dst': 'two'},
            {'name': 'two', 'src': 'two', 'dst': 'two'},
            {'name': 'home', 'src': 'two', 'dst': 'home'}
            ]
        }

