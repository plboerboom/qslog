from qslog import transition
from qslog import Error

import dateutil.parser
import datetime
import re
import pprint
import json
import jsonschema
import tzlocal
import pytz


def parse_entry(s):

    fields = s.split()

    if len(fields) < 4:
        raise Error("insufficient fields")

    typ = fields[0]
    typ_re = r'(beer$)|(wine$)'
    if not re.match(typ_re, typ):
        raise Error('Unrecognized type \'%s\'' % typ)

    try:
        quant = float(fields[1])
    except ValueError:
        raise Error('Quantity must be a number')

    units = fields[2]

    units_re = '|'.join([
        '(oz\.?$)',
        '(ounces?$)',
        '(ml$)',
        '(milliliters?$)',
        '(liters?$)',
        '(cups?$)',
        '(quarts?$)',
        '(gallons?$)'
        ])
    if not re.match(units_re, units):
        raise Error('Unrecognized unit \'%s\'' % units)

    try:
        abv = float(fields[3])
    except ValueError:
        raise Error('ABV must be a number.')

    entry = {'volume': {'quantity': quant, 'units': units},
             'type': typ, 'abv': abv}

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
    ltz = tzlocal.get_localzone()

    if line.strip() == '':
        dt = ltz.localize(datetime.datetime.now()).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
                )
    else:
        try:
            dt = ltz.localize(dateutil.parser.parse(line))
        except ValueError:
            raise

    self.record = {'datetime': dt.isoformat()}


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
    print json.dumps(self.record)


state_config = {
    'initial': {'state': 'home', 'defer': True},
    'events': [
        {'name': 'log', 'src': 'home', 'dst': 'log'},
        {'name': 'save', 'src': 'log', 'dst': 'home'},
        {'name': 'add', 'src': 'log', 'dst': 'log'}
    ]
}

# TODO: Write data
# TODO: Autocomplete
