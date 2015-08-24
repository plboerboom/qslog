import types

def onstartup(e):
    print 'starting up'

def onenterhome(e):
    print 'entering home'
    setattr(e.command, 'do_session', types.MethodType(do_session, e.command))
    
def onenterwaiting_exercise(e):
    e.command.prompt = 'exercise: '

def do_session(self, line):
    print 'in session'
    self.state_machine.start_session(command = self)

state_config = {
        'initial': {'state': 'home', 'defer': True},
        'events': [
            {'name': 'start_session', 'src' : 'home', 'dst' : 'waiting_exercise'},
            {'name': 'abort', 'src': 'waiting_exercise', 'dst': 'home'},
            {'name': 'done', 'src' : 'workout', 'dst': 'home'},
            {'name': 'done', 'src': 'alco', 'dst': 'home'}
            ],
        'callbacks': {
            'onstartup': onstartup,
            'onenterhome': onenterhome,
            'onenterwaiting_exercise': onenterwaiting_exercise
            }
        }

