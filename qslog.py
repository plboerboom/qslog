#! /usr/bin/env python

import types
import cmd
import readline
import inspect

import fysom

def transition(f):
    def inner(self, line):
        smf = getattr(self.state_machine, f.__name__.replace('do_', ''))
        smf()
        print self.state_machine.current
        #self.state_machine.goto_one()
        return f(self, line)
    return inner

class Command(cmd.Cmd):
    def __init__(self):
        import config

        print config.state_config

        self.state_machine = fysom.Fysom(config.state_config)

        command = self

        # fysom's internal map is {event: {src: 'src', dst: 'dst}}
        # we need a lookup from src states to valid events.
        state_map = {}
        for ev, mp in self.state_machine._map.iteritems():
            for src in mp:
                state_map.setdefault(src, []).append(ev)

        # We want the event to include the cmd object so that
        # it is accessible to the user-defined transition function.
        # To make it so, we 'patch' fysom's before_event method,
        # which is the first in its sequence of hooks.
        def new_before_event(self, e):
            e.command = command

            fnname = 'onbefore' + e.event
            if hasattr(self, fnname):
                return getattr(self, fnname)(e)

        fysom.Fysom._before_event = new_before_event
        
        # We want to attach and detach commands to cmd
        # when transitioning states. To do so, we
        # 'patch' fysom's enter state method
        def new_enter_state(self, e):
            # attach the cmd object to the event so it
            # is accessible from user-defined transition functions
            e.command = command
            
            # detach all 'do_*' functions defined in config
            for nm in vars(config):
                if nm.startswith('do_') and hasattr(command, nm):
                    delattr(command, nm)

            # look up new state in our map
            if e.dst in state_map:
                # look up valid events for new state
                for ev in state_map[e.dst]:
                    fname = 'do_' + ev
                    # look for functions in config that match the valid events
                    if fname in vars(config):
                        f = getattr(config, fname)
                        if hasattr(f, '__call__'):
                            setattr(command, fname, types.MethodType(f, command)) 
            
            # original method code
            for fnname in ['onenter' + e.dst, 'on' + e.dst]:
                if hasattr(self, fnname):
                    return getattr(self, fnname)(e)

        fysom.Fysom._enter_state = new_enter_state

        self.state_machine.startup()
        cmd.Cmd.__init__(self)

    def do_q(self, line):
        return True

    def do_EOF(self, line):
        return True



if __name__ == '__main__':

    Command().cmdloop()

