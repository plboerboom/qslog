#! /usr/bin/env python

import argparse
import json

import jsonschema

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('schema')
    parser.add_argument('instance')
    args = parser.parse_args()

    with open(args.schema) as f:
        try:
            schema = json.load(f)
        except:
            raise

    with open(args.instance) as f:
        try:
            instance = json.load(f)
        except:
            raise

    try:
        jsonschema.validate(instance, schema)
    except (jsonschema.exceptions.ValidationError) as e:
        print e
