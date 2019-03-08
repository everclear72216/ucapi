"""
Device Configuration.

Usage:
    devconf.py -o OUTPUT FILES
    devconf.py --version

Options:
    -I --import-dir PATH
        Adds a directory to the list of import directories.
    -o --output OUTPUT
        The name of the header file to be created.
"""

import os
import sys
import docopt
import tomlkit

DEVCONF_VERSION_MAJOR=0
DEVCONF_VERSION_MINOR=0
DEVCONF_VERSION_PATCH=1
DEVCONF_VERSION = (DEVCONF_VERSION_MAJOR, DEVCONF_VERSION_MINOR, DEVCONF_VERSION_PATCH)
DEVCONV_VERSION_STRING='%d.%d.%d' % DEVCONF_VERSION

def is_container(arg):
    is_container = True;

    for key in arg.keys():
        if not isinstance(arg[key], dict):
            is_container = False
            break

    return is_container

def is_entry(arg):
    is_entry = True

    for key in arg.keys():
        if isinstance(arg[key], dict):
            is_entry = False
            break

    return is_entry

class DeviceConfigurationException(BaseException):
    def __init__(self, message):
        self.message = str(message)

class ConfigurationEntry(object):
    VALUE_KEY = 'value'

    def __init__(self, path, definition, value):
        self.value = value
        self.path = str(path)
        self.definition = definition

    def get_path(self):
        return str(self.path)

    def update(self, **value):
        self.value = value.get(self.VALUE_KEY, None)

    def validate(self):
        if self.value is None:
            raise DeviceConfigurationException('entry requires value')

        self.definition.validate(self.value)

    def setvalue(self):
        return self.value

    def usevalue(self):
        return self.definition.usevalue(self.value)

    def generate(self):
        result = []

        result.append(self.definition.generate())

        valname = self.path.upper()
        val = '%s_%s' % (self.path.upper(), str(self.value).upper())
        define = '#define %s %s' % (valname, val)
        define = define.replace('.', 'P')
        result.append(define)

        valname = '%s_VALUE' % (valname)
        val = '%s_VALUE' % (val)
        define = '#define %s %s' % (valname, val)
        define = define.replace('.', 'P')
        result.append(define)

        result.append('')
        
        return os.linesep.join(result)

class ConfigurationDefinitions(object):
    DEFAULT_VALUE_KEY = 'default_value'
    ALLOWED_VALUES_KEY = 'allowed_values'

    SET_VALUE_INDEX = 0
    USE_VALUE_INDEX = 1

    def __init__(self, path, **definition):
        self.path = str(path)
        self.default_value = definition.get(self.DEFAULT_VALUE_KEY, None)
        self.allowed_values = definition.get(self.ALLOWED_VALUES_KEY, [[],[]])

    def default(self):
        return ConfigurationEntry(self.path, self, self.default_value)

    def usevalue(self, value):
        setvalues = self.allowed_values[self.SET_VALUE_INDEX]
        usevalues = self.allowed_values[self.USE_VALUE_INDEX]

        return usevalues[setvalues.index(value)]

    def setvalue(self, value):
        setvalues = self.allowed_values[self.SET_VALUE_INDEX]
        usevalues = self.allowed_values[self.USE_VALUE_INDEX]

        return setvalues[usevalues.index(value)]

    def generate(self):
        setvalues = self.allowed_values[self.SET_VALUE_INDEX]

        result = []
        for setval in setvalues:
            val = self.usevalue(setval)
            valname = '%s_%s' % (self.path.upper(), str(setval).upper())
            if isinstance(val, str):
                define = '#define %s "%s"' % (valname, val)
            else:
                define = '#define %s %s' % (valname, val)
            define = define.replace('.', 'P')
            result.append(define)

            valname = '%s_VALUE' % (valname)
            if isinstance(setval, str):
                define = '#define %s "%s"' % (valname, setval)
            else:
                define = '#define %s %s' % (valname, setval)
            define = define.replace('.', 'P')
            result.append(define)

        return os.linesep.join(result)

    def validate(self, value):
        if value not in self.allowed_values[self.SET_VALUE_INDEX]:
            message = 'value %s is not allwed for %s' % (value, self.path)
            raise DeviceConfigurationException(message)

class DeviceConfiguration(object):
    def __init__(self, filename):
        self.entries = []
        self.definitions = []
        self.filename = str(filename)

    def get_entries(self):
        return self.entries

    def get_filename(self):
        return str(self.filename)

    def get_definitions(self):
        return self.definitions

    def get_entry(self, path):
        return next((entry for entry in self.entries if entry.get_path() == path), None)

    def update_definitions(self, data, path):
        if not isinstance(data, dict):
            message = 'data must be a dict'
            raise DeviceConfigurationException(message)

        if not isinstance(path, list):
            message = 'path must be a list'
            raise DeviceConfigurationException(message)

        entry = is_entry(data)
        container = is_container(data)

        if container and not entry:
            for key in data.keys():
                p = path.copy()
                p.append(key)
                self.update_definitions(data[key], p)

        elif entry and not container:
            definition = ConfigurationDefinitions('_'.join(path), **data)

            self.definitions.append(definition)
            self.entries.append(definition.default())

        else:
            if container and entry:
                message = 'neither entry nor container at key %s' % (path)
                raise DeviceConfigurationException(message)

            else:
                message = 'cannot determine type of entry at key %s' % (path)
                raise DeviceConfigurationException(message)

    def update_entries(self, data, path):
        if not isinstance(data, dict):
            message = 'data must be a dict'
            raise DeviceConfigurationException(message)

        if not isinstance(path, list):
            message = 'path must be a list'
            raise DeviceConfigurationException(message)

        entry = is_entry(data)
        container = is_container(data)

        if container and not entry:
            for key in data.keys():
                p = path.copy()
                p.append(key)
                self.update_entries(data[key], p)

        elif entry and not container:
            entry = self.get_entry('_'.join(path))
            if entry is not None:
                entry.update(**data)
            else:
                message = 'No entry for path %s' % ('_'.join(path))
                raise DeviceConfigurationException(message)

        else:
            if container and entry:
                message = 'neither entry nor container at key %s' % (path)
                raise DeviceConfigurationException(message)

            else:
                message = 'cannot determine type of entry at key %s' % (path)
                raise DeviceConfigurationException(message)

    def validate(self):
        for entry in self.entries:
            entry.validate()

    def generate(self, filename):
        with open(filename, 'w+') as file:
            for entry in self.entries:
                file.write('%s%s' % (entry.generate(), os.linesep))

    def load(self):
        document = ''

        with open(self.filename, 'rt') as file:
            document = file.read();

        toml = tomlkit.parse(document)

        data = dict(toml)
        defs = data.pop('def', {})

        self.update_definitions(defs, [])
        self.update_entries(data, [])

def main(args):
    config = DeviceConfiguration(args['FILES'])

    config.load()
    config.validate()
    config.generate(args['--output'])

    return 0

if __name__ == '__main__':
    try:
        args = docopt.docopt(__doc__, version=DEVCONV_VERSION_STRING)
        exit(main(args))
    except DeviceConfigurationException as exc:
        print(exc)
        exit(1)
