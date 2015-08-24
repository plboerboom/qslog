#! /usr/bin/env python

import ast
import types
import cmd
import readline
import inspect

import fysom

## It's unclear whether the cmd framework will work for what we need to do.
## We need:
##   - to be able to create the language it understands at runtime
##   - to be able to accept just values in some contexts (not mandatory)

## the user config is essentially describing a state machine for the interpreter.


## create function at runtime
myf_ast = ast.FunctionDef(
        name = 'f',
        args = ast.arguments(args = [ast.Name(id='a', ctx=ast.Param())],
                             vararg = None, kwarg = None, defaults = []
                            ),
        body = [ast.Print(dest=None,
                          values=[ast.Num(n=42)],
                          nl = True)
               ],
        decorator_list = [],
)

ast.fix_missing_locations(myf_ast)

mod_ast = ast.Module(body=[myf_ast])
mod_code = compile(mod_ast, 'notafile', 'exec')

myf_code = [c for c in mod_code.co_consts if isinstance(c, types.CodeType)][0]

myf = types.FunctionType(myf_code, {})


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

class Command(cmd.Cmd):
    def __init__(self, config):
        self.state_machine = fysom.Fysom(config)
        self.state_machine.startup(command = self)
        cmd.Cmd.__init__(self)

        # attach function at runtime
        #setattr(self, 'do_f', myf)
#        delattr(self, 


    def do_abort(self, line):
        self.state_machine.abort(cmd = self)

    def do_ex(self, line):
        print line

    def do_q(self, line):
        return True

    def do_EOF(self, line):
        return True



######################


if __name__ == '__main__':

    Command(state_config).cmdloop()

    sm = fysom.Fysom({'initial': 'home',
                    'events': [
                        {'name': 'wo', 'src' : 'home', 'dst' : 'workout'},
                        {'name': 'alc', 'src' : 'home', 'dst' : 'alco'},
                        {'name': 'done', 'src' : 'workout', 'dst': 'home'},
                        {'name': 'done', 'src': 'alco', 'dst': 'home'}
                        ],
                    'callbacks': {
                        'onenterworkout': onenterwo,
                        'onwo': onwo
                        }
                    })
