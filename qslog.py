#! /usr/bin/env python

import types
import cmd
import readline

import fysom

def transition(f):
    def inner(self, line):
        smf_name = f.__name__.replace('do_', '')

        res = f(self, line)

        if hasattr(self.state_machine, smf_name):
            smf = getattr(self.state_machine, smf_name)
            if hasattr(smf, '__call__'):
                try:
                    smf()
                except fysom.Canceled:
                    pass

        return res
    return inner

class Command(cmd.Cmd):
    def __init__(self):
        import config

        # Automatically add callbacks defined in config.
        event_callback_prefixes = [ 'onbefore', 'onafter' ]
        state_callback_prefixes = [ 'onleave', 'onenter', 'onreenter' ]

        event_names = [e['name'] for e in config.state_config['events']]
        state_names = set(
                [
                state for sublist in
                [[e['src'], e['dst']] for e in config.state_config['events']]
                for state in sublist
                ]
                )

        config.state_config['callbacks'] = {}
        callbacks = config.state_config['callbacks']

        for event_name in event_names:
            for prefix in event_callback_prefixes:
                fname = prefix + event_name
                if hasattr(config, fname):
                    f = getattr(config, fname)
                    if hasattr(f, '__call__'):
                        callbacks[fname] = f

        for state_name in state_names:
            for prefix in state_callback_prefixes:
                fname = prefix + state_name
                if hasattr(config, fname):
                    f = getattr(config, fname)
                    if hasattr(f, '__call__'):
                        callbacks[fname] = f

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

        # cmd.Cmd's 'help' uses its get_names method to display
        # available commands. But get_names uses dir() on the class,
        # so only sees the names defined statically in the source.
        # We patch it to make it recognize the dynamically added commands.
        def new_get_names(self):
            return vars(self).keys() + dir(self.__class__)

        cmd.Cmd.get_names = new_get_names

        cmd.Cmd.__init__(self)

    def do_smcurr(self, line):
        print self.state_machine.current

    def do_q(self, line):
        return True

    def do_EOF(self, line):
        return True



if __name__ == '__main__':

    Command().cmdloop()

