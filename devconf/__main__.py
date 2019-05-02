"""
Device Configuration.

Usage:
    devconf.py -o OUTPUT FILE
    devconf.py --version

Options:
    -o --output OUTPUT
        The name of the header file to be created.
"""

import docopt
import generator
import parser.parser

DEVCONF_VERSION_MAJOR = 0
DEVCONF_VERSION_MINOR = 0
DEVCONF_VERSION_PATCH = 1
DEVCONF_VERSION = (DEVCONF_VERSION_MAJOR, DEVCONF_VERSION_MINOR, DEVCONF_VERSION_PATCH)
DEVCONF_VERSION_STRING = '%d.%d.%d' % DEVCONF_VERSION


class DeviceConfiguration(object):
    def __init__(self, infile: str, outfile: str):
        self._infile = str(infile)
        self._outfile = str(outfile)

    def compile(self) -> None:
        with open(self._infile, 'rt') as file:
            document = file.read()

            p = parser.parser.Parser(self._infile)

            syntax_tree, symbol_table = p.parse(document, tracking=True)

            gen = generator.MacroGenerator(syntax_tree, symbol_table)
            gen.generate(self._outfile)


def main(args):
    config = DeviceConfiguration(args['FILE'], args['--output'])
    config.compile()

    return 0


if __name__ == '__main__':
    exit(main(docopt.docopt(__doc__, version=DEVCONF_VERSION_STRING)))
