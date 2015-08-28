from qslog import transition
from qslog import Error

import dateutil.parser
import datetime
import re
import pprint

def parse_entry(s):
    fields = s.split()

    if len(fields) < 4:
        raise Error("insufficient fields")

    # TODO: validate
    # TODO: return structured entry
    typ = fields[0]

    try:
        quant = float(fields[1])
    except ValueError:
        raise Error('non-numeric quantity')

    units = fields[2]
    abv = fields[3]

    entry = { 'volume': { 'quantity': quant, 'units': units },
            'type': typ, 'abv': abv }
    return entry

def onenterhome(e):
    e.command.prompt = '> '
    
def onenterlog(e):
    pprint.pprint(e.command.record)
    e.command.prompt = '>> '

def onreenterlog(e):
    pprint.pprint(e.command.record)

def onbeforelog(e):
    try:
        e.command.record
    except AttributeError:
        return False
    
@transition
def do_log(self, line):
    if line.strip() == '':
        date = datetime.datetime.now()
    try:
        date = dateutil.parser.parse(line)
    except ValueError:
        return

    self.record = { 'datetime': date }

def onbeforeadd(e):
    try:
        entry = parse_entry(e.command.line)
    except Error as e:
        print e
        return False


    e.command.record.setdefault('entries', []).append(entry)

@transition
def do_add(self, line):
    self.line = line
    pass

@transition
def do_save(self, line):
    pass


state_config = {
        'initial': {'state': 'home', 'defer': True},
        'events': [
            {'name': 'log', 'src' : 'home', 'dst' : 'log'},
            {'name': 'save', 'src': 'log', 'dst': 'home'},
            {'name': 'add', 'src' : 'log', 'dst': 'log'}
            ]
        }

# TODO: Write data
# TODO: Autocomplete
