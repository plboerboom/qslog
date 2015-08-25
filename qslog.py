#! /usr/bin/env python

import ast
import types
import cmd
import readline
import inspect

import fysom

class Command(cmd.Cmd):
    def __init__(self):
        import config

        self.state_machine = fysom.Fysom(config.state_config)

        command = self

        state_map = {}
        for ev, mp in self.state_machine._map.iteritems():
            for src in mp:
                state_map.setdefault(src, []).append(ev)

        def new_enter_state(self, e):
            print 'patched!'
            e.command = command
            
            for nm in vars(config):
                if nm.startswith('do_') and hasattr(command, nm):
                    delattr(command, nm)

            if e.dst in state_map:
                print state_map[e.dst]
                for ev in state_map[e.dst]:
                    fname = 'do_' + ev
                    if fname in vars(config):
                        print 'found it!'
                        print getattr(config, fname)
                        f = getattr(config, fname)
                        setattr(command, fname , types.MethodType(f, command)) 

            for fnname in ['onenter' + e.dst, 'on' + e.dst]:
                if hasattr(self, fnname):
                    return getattr(self, fnname)(e)

        fysom.Fysom._enter_state = new_enter_state

        self.state_machine.startup()
        cmd.Cmd.__init__(self)

        # attach function at runtime
        #setattr(self, 'do_f', myf)
#        delattr(self, 



    def do_q(self, line):
        return True

    def do_EOF(self, line):
        return True



######################


if __name__ == '__main__':

    Command().cmdloop()

