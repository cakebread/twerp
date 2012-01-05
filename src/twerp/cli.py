# PPylint: disable-msg=W0613,W0612,W0212,W0511,R0912,C0322,W0704
# W0511 = XXX (my own todo's)

"""

cli.py
======

Desc: Command-line module

Author: Rob Cakebread <cakebread a t gmail.com>

License : BSD

"""

__docformat__ = 'restructuredtext'


import os
import sys
import optparse
import logging

from configobj import ConfigObj
from clint.textui import colored, puts, indent

from twerp.__init__ import __version__ as VERSION
from twerp.mytwilio import send_sms, list_sms, get_sms_sid, list_numbers


class Twerp(object):

    """
    Main class for twerp optparse CLI
    """

    def __init__(self):
        self.options = None
        self.logger = logging.getLogger("twerp")

    def set_log_level(self):
        """
        Set log level according to command-line options

        @returns: logger object
        """

        if self.options.debug:
            self.logger.setLevel(logging.DEBUG)
        elif self.options.quiet:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        return self.logger

    def run(self):
        """
        Perform actions based on CLI options

        @returns: status code
        """
        opt_parser = setup_opt_parser()
        (self.options, remaining_args) = opt_parser.parse_args()
        logger = self.set_log_level()
        if self.options.numbers:
            list_numbers(self.options.verbose)
        elif self.options.listsms:
            list_sms()
        elif self.options.twerp_version:
            return self.twerp_version()
        elif self.options.sid:
            get_sms_sid(self.options.sid)
        elif self.options.sms:
            send_sms([self.options.recipient], self.options.sms,
            self.options.verbose)
        else:
            opt_parser.print_help()

    def twerp_version(self):
        """
        Show twerp's version

        @returns: 0
        """
        self.logger.info("twerp version %s" % VERSION)
        return 0


def setup_opt_parser():
    """
    Setup the optparser

    @returns: opt_parser.OptionParser

    """
    #pylint: disable-msg=C0301
    #line too long

    usage = "usage: %prog [options]"
    opt_parser = optparse.OptionParser(usage=usage)

    opt_parser.add_option("--version", action='store_true',
            dest="twerp_version", default=False,
            help="Show twerp version and exit.")
    opt_parser.add_option("-v", "--verbose", action='store_true',
            dest="verbose", default=False, help="Show more output stuff.")

    opt_parser.add_option("-s", "--sms", action='store',
            dest="sms", default=False, help="Send SMS text message")

    opt_parser.add_option("-r", "--recipient", action='store',
            dest="recipient", default=False, help="Number to call or SMS.")

    opt_parser.add_option("--debug", action='store_true',
            dest="debug", default=False, help="Show debugging information.")

    opt_parser.add_option("-q", "--quiet", action='store_true',
            dest="quiet", default=False, help="Show less output.")
    #Reporting options:
    opt_parser.add_option("-L", "--list-sms", action='store_true',
            dest="listsms", default=False, help="List incoming SMS messages.")

    opt_parser.add_option("-N", "--numbers", action='store_true',
            dest="numbers", default=False,
            help="Show all my Twilio phone numbers")

    opt_parser.add_option("-S", "--SID", action='store',
            dest="sid", default=False, help="Show log for given SID")

    return opt_parser


def main():
    """
    Let's do it.
    """
    my_twerp = Twerp()
    my_twerp.run()

if __name__ == "__main__":
    sys.exit(main())
