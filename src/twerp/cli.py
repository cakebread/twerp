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
import cmd
import sys
import optparse
import logging

from configobj import ConfigObj
from clint.textui import colored, puts, indent

from twerp.__init__ import __version__ as VERSION
from twerp.mytwilio import (send_sms, list_sms, get_sms_sid,
        list_numbers, list_calls, call_numbers, call_url)


class Interactive(cmd.Cmd):
    """Simple command processor example."""
    def __init__(self, sid=None, callerid=None):
        cmd.Cmd.__init__(self)
        self.sid = sid
        self.callerid = callerid

    def cmdloop(self, sid=None, callerid=None):
        intro = "Type 'help' for twerp commands"
        if self.sid:
            self.prompt = "twerp (SID:%s...%s) [%s]) >> " % (self.sid[0:5], self.sid[:-3], self.callerid)
        else:
            self.prompt = "twerp >> "
        return cmd.Cmd.cmdloop(self, intro)    

    def do_list(self, args=None):
        list_calls()

    def do_sid(self, sid):
        if sid:
            self.sid = sid
        else:
            print "You must specify the SID to use."

    def do_url(self, url):
        if url:
            call = call_url(self.sid, url)
            print dir(call)
            #self.callerid = call.callerid
            print call.status
        else:
            print "You need to specify a valid TWML URL e.g. http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient"
    
    def do_EOF(self, line):
        return True

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
            return list_numbers(self.options.verbose)
        elif self.options.dial:
            if not self.options.url:
                logger.error("You must specify a --url with TWML")
                return 1
            numbers = self.options.dial.split(",")
            sid, callerid = call_numbers(numbers, self.options.verbose,
                    self.options.callerid, self.options.url,
                    self.options.interactive)
            Interactive(sid=sid, callerid=callerid).cmdloop()
        elif self.options.listsms:
            return list_sms()
        elif self.options.twerp_version:
            return self.twerp_version()
        elif self.options.sid:
            return get_sms_sid(self.options.sid)
        elif self.options.sms_recipients:
            numbers = self.options.sms_recipients.split(",")
            return send_sms(numbers, self.options.sms_message,
                    self.options.verbose)
        else:
            opt_parser.print_help()
        return 0

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

    opt_parser.add_option("--V", "--version", action="store_true",
            dest="twerp_version", default=False,
            help="Show twerp version and exit.")
    opt_parser.add_option("-v", "--verbose", action='store_true',
            dest="verbose", default=False, help="Show more output stuff.")

    opt_parser.add_option("--debug", action='store_true',
            dest="debug", default=False, help="Show debugging information.")

    opt_parser.add_option("-q", "--quiet", action='store_true',
            dest="quiet", default=False, help="Show less output.")

    group_common = optparse.OptionGroup(opt_parser,
            "Common options",
            "These options can be used for both SMS and voice calls.")

    group_common.add_option("-c", "--callerid", action='store',
            dest="callerid", default=None,
            help="Phone number you are calling from or texting from.")

    group_sms = optparse.OptionGroup(opt_parser,
            "SMS options",
            "Send and reveive SMS text messages.")
    group_sms.add_option("-m", "--message", action='store',
            metavar="<TXT MSG>",
            dest="sms_message", default=False, help="Send SMS text message")

    group_sms.add_option("-s", "--sms", action='store',
            dest="sms_recipients", default=False,
            metavar="+12135551212,+14155551212",
            help="Send SMS text message to list of numbers.")

    group_sms.add_option("-l", "--list-sms", action='store_true',
            dest="listsms", default=False, help="Show incoming SMS messages.")

    group_call = optparse.OptionGroup(opt_parser,
            "Voice call options",
            "Place phone calls, execute TWIML.")
    group_call.add_option("-d", "--dial", action='store',
            metavar="+12135551212,+14155551212",
            help="List of numbers to dial, comma-separated.",
            dest="dial", default=False)

    group_call.add_option("-i", "--interactive", action='store_true',
            help="Go into interactive command-line mode after dialing.",
            dest="interactive", default=False)

    group_call.add_option("-u", "--url", action='store',
            metavar="URL of TWIML",
            dest="url", default=False, help="URL of TWIML to pass call with --call")

    group_reports = optparse.OptionGroup(opt_parser,
            "Reporting options",
            "List your Twilio phone numbers and detailed information about each.")

    group_reports.add_option("-N", "--numbers", action='store_true',
            dest="numbers", default=False, help="Show all my Twilio phone " +                
            "numbers. Use -Nv for detailed info on each number.") 
    group_reports.add_option("-S", "--SID", action='store',
            dest="sid", default=False, help="Show log for given SID")

    opt_parser.add_option_group(group_common)
    opt_parser.add_option_group(group_sms)
    opt_parser.add_option_group(group_call)
    opt_parser.add_option_group(group_reports)
    return opt_parser


def main():
    """
    Let's do it.
    """
    my_twerp = Twerp()
    my_twerp.run()

if __name__ == "__main__":
    sys.exit(main())
