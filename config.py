import types

def onstartup(e):
    print 'starting up'

def onenterhome(e):
    e.command.prompt = 'home: '
    
def onenterone(e):
    e.command.prompt = 'one: '

def do_goto_one(self, line):
    print line
    self.state_machine.goto_one()

def do_abort(self, line):
    self.state_machine.abort()

def onentertwo(e):
    e.command.prompt = 'two: '

def do_goto_two(self, line):
    self.state_machine.goto_two()

def do_goto_home(self, line):
    self.state_machine.goto_home()


state_config = {
        'initial': {'state': 'home', 'defer': True},
        'events': [
            {'name': 'goto_one', 'src' : 'home', 'dst' : 'one'},
            {'name': 'abort', 'src': 'one', 'dst': 'home'},
            {'name': 'goto_two', 'src' : 'one', 'dst': 'two'},
            {'name': 'goto_two', 'src': 'two', 'dst': 'two'},
            {'name': 'goto_home', 'src': 'two', 'dst': 'home'}
            ],
        'callbacks': {
            'onstartup': onstartup,
            'onenterhome': onenterhome,
            'onenterone': onenterone,
            'onentertwo': onentertwo
            }
        }

