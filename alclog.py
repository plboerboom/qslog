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
import os.path

schema_path = 'alc.schema.json'
userid = 'plboerboom'
local_data_path = 'alclog-data'

normalize_units = {
        'oz': 'ounce',
        'oz.': 'ounce',
        'ounce': 'ounce',
        'ounces': 'ounce',
        'ml': 'milliliter',
        'milliliter': 'milliliter',
        'milliliters': 'milliliter',
        'liter': 'liter',
        'liters': 'liter',
        'cup': 'cup',
        'cups': 'cup',
        'quart': 'quart',
        'quarts': 'quart',
        'gallon': 'gallon',
        'gallons': 'gallon'
        }

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

    units = normalize_units[units]

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

    self.record = {'datetime': dt.isoformat(), 'userid': userid}


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
    with open(schema_path) as f:
        try:
            schema = json.load(f)
        except:
            raise

    try:
        jsonschema.validate(self.record, schema)
    except (jsonschema.exceptions.ValidationError) as e:
        print e

    # TODO: check that path exists
    filename = self.record['datetime'].replace(':','_') + '.json'
    filepath = os.path.join(local_data_path, filename)
    with open(filepath, 'w') as f:
        print json.dump(self.record, f)


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
