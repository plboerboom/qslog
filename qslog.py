#! /usr/bin/env python

import ast
import types
import cmd
import readline

import fysom

## It's unclear whether the cmd framework will work for what we need to do.
## We need:
##   - to be able to create the language it understands at runtime
##   - to be able to accept just values in some contexts (not mandatory)

## the user config is essentially describing a state machine for the interpreter.

def onenterwo(e):
    print 'entering wo'
    print e

def onwo(e):
    print 'on wo'
    print e

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

def do_sets(line):
    print 'sets'
    print line

class Command(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        # attach function at runtime
        setattr(self, 'do_f', myf)

    def do_w(self, msg):
        self.prompt = 'reps: '
        setattr(self, 'do_sets', do_sets)
        print msg

    def do_q(self, line):
        return True

    def do_EOF(self, line):
        return True

