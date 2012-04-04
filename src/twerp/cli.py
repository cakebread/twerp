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


import cmd
import sys
import optparse
import logging
from urllib import quote_plus

from clint.textui import colored

from twerp.__init__ import __version__ as VERSION
from twerp.twilio_support import RestClient


class Interactive(cmd.Cmd):
    """Cmmand processor"""
    def __init__(self, client, sid=None):
        cmd.Cmd.__init__(self)
        self.sid = sid
        self.logger = logging.getLogger("twerp")
        self.client = client

    def emptyline(self):
        return

    def postloop(self):
        '''Print a blank line after program exits interactive mode'''
        print '\n'

    def cmdloop(self, sid=''):
        intro = "Type 'help' for twerp commands"
        self.sid = sid
        if self.sid is not None:
            self.prompt = "twerp (%s) >> " % self.sid[0:7]
        else:
            self.prompt = "twerp (...) >> "
        try:
            return cmd.Cmd.cmdloop(self, sid)
        except KeyboardInterrupt:
            sys.exit(0)

    def do_info(self, sid=None):
        '''
        Display info for current SID
        '''
        if not sid:
            sid = self.sid
        if sid:
            self.client.sid_call(sid)
        else:
            self.logger.error("Need an SID")

    def do_hangup(self, arg=None):
        '''
        Hangs up call associated with current SID shown in prompt.
        '''
        self.client.hangup(self.sid)
        self.prompt = "twerp (...) >> "

    def do_nuke(self, arg=None):
        '''
        Hangs up all voice calls in progress for the entire account
        CAUTION: Read the above carefully.
        '''
        self.client.hangup_all_calls()
        self.prompt = "twerp (...) >> "

    def do_list(self, args=None):
        '''
        List all calls in progress for your account
        '''
        self.client.list_calls()

    def do_sid(self, sid):
        '''
        Change SID for interactive session. New SID shows in prompt.
        '''
        if sid:
            self.sid = sid
            self.prompt = colored.red("twerp (%s...) >> " % self.sid[0:7])
        else:
            print >> sys.stderr, "You must specify the SID to use."

    def do_forward(self, number):
        '''
        Forward call to another phone number. e.g.
        forward +13235551212
        '''
        if number:
            url = '''http://twimlets.com/forward?PhoneNumber='''
            text = quote_plus(number)
            url = '%s%s' % (url, number)
            print url
            call = self.client.call_url(self.sid, url)
            #print >> sys.stderr, call.status

    def do_url(self, url):
        '''
        Redirect call using TwiML at URL e.g.
        url http://twimlets.com/some.twml
        '''
        if url:
            call = self.client.call_url(self.sid, url)
            #print >> sys.stderr, call.status
        else:
            print >> sys.stderr, "You need to specify a valid TWML URL e.g. "
            print >> sys.stderr, \
                "http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient"

    def do_EOF(self, line):
        '''Exit twerp's interactive mode'''
        return True


class Twerp(object):

    """
    Main class for twerp optparse CLI
    """

    def __init__(self):
        self.options = None
        self.client = RestClient()

    def set_log_level(self):
        """
        Set log level according to command-line options

        @returns: logger object
        """
        log_format = '%(message)s'

        logging.basicConfig(level=logging.ERROR, format=log_format)
        logger = logging.getLogger("twerp")

        if self.options.debug:
            logger.setLevel(logging.DEBUG)
        elif self.options.verbose:
            logger.setLevel(logging.INFO)
        return logger

    def run(self):
        """
        Perform actions based on CLI options

        @returns: status code
        """
        opt_parser = setup_opt_parser()
        (self.options, remaining_args) = opt_parser.parse_args()
        self.logger = self.set_log_level()

        if self.options.numbers:
            return self.client.list_numbers(self.options.verbose)
        elif self.options.dial:
            if not self.options.url and not self.options.say:
                self.logger.error("You must specify a --url with TwiML " +
                    "or --say something")
                return 1
            numbers = self.options.dial.split(",")
            sid = self.client.call_numbers(numbers, self.options.verbose,
                    self.options.callerid, self.options.url,
                    self.options.say)
            if self.options.interactive:
                Interactive(self.client).cmdloop(sid)
                return
        elif self.options.conference:
            if not self.options.room:
                self.logger.error("You must specify a --room to join.")
                return 1
            numbers = self.options.conference.split(",")
            sid = self.client.create_conference(numbers,
                    self.options.room,
                    self.options.verbose,
                    self.options.callerid)
            if self.options.interactive:
                Interactive(self.client).cmdloop(sid)
            return
        elif self.options.purchase:
            return self.client.purchase_number(self.options.purchase)
        elif self.options.contains and self.options.areacode:
            return self.client.numbers_contain_areacode(
                    self.options.areacode,
                    self.options.contains)
        elif self.options.contains:
            return self.client.numbers_contain(self.options.contains)
        elif self.options.areacode:
            return self.client.search_numbers(self.options.areacode)
        elif self.options.rename_account:
             self.client.rename_account(self.options.rename_account)
        elif self.options.list_accounts:
             self.client.list_accounts()
        elif self.options.rename_account:
             self.client.create_subaccount(self.options.create_subaccount)
        elif self.options.applications:
            return self.client.list_applications()
        elif self.options.participants:
            return self.client.list_conference_participants()
        elif self.options.conferences:
            return self.client.list_conferences()
        elif self.options.listsms:
            return self.client.list_sms()
        elif self.options.twerp_version:
            return self.twerp_version()
        elif self.options.sid:
            return self.client.get_sms_sid(self.options.sid)
        elif self.options.sms_recipients:
            numbers = self.options.sms_recipients.split(",")
            return self.client.send_sms(numbers, self.options.sms_message,
                    self.options.verbose)
        elif self.options.notifications:
            return self.client.notifications(self.options.verbose)
        elif self.options.interactive:
            Interactive(self.client).cmdloop('')
            return
        else:
            opt_parser.print_help()
        return 1

    def twerp_version(self):
        """
        Show twerp's version

        @returns: None
        """
        print("twerp version %s" % VERSION)


def setup_opt_parser():
    """
    Setup the optparser

    @returns: opt_parser.OptionParser

    """

    usage = "usage: %prog [options]"
    opt_parser = optparse.OptionParser(usage=usage)

    opt_parser.add_option("--version", action="store_true",
            dest="twerp_version", default=False,
            help="Show twerp version and exit.")

    opt_parser.add_option("-v", "--verbose", action='store_true',
            dest="verbose", default=False, help="Show more output stuff.")

    opt_parser.add_option("--debug", action='store_true',
            dest="debug", default=False, help="Show debugging information.")

    opt_parser.add_option("-q", "--quiet", action='store_true',
            dest="quiet", default=False, help="Show less output.")

    #Common
    group_common = optparse.OptionGroup(opt_parser,
            "Common options",
            "These options can be used for both SMS and voice calls.")

    group_common.add_option("-c", "--callerid", action='store',
            dest="callerid", default=None,
            help="Phone number you are calling from or texting from.")

    group_common.add_option("-i", "--interactive", action='store_true',
            help="Go into interactive command-line mode after " +
            "dialing (voice or conferences).",
            dest="interactive", default=False)

    #SMS
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

    #Calls (voice)
    group_call = optparse.OptionGroup(opt_parser,
            "Voice call options",
            "Place phone calls, execute TWIML.")

    group_call.add_option("-d", "--dial", action='store',
            metavar="+12135551212,+14155551212",
            help="List of numbers to dial, comma-separated.",
            dest="dial", default=False)

    group_call.add_option("-y", "--say", action='store',
            metavar="Say something.",
            dest="say", default=False,
            help="Use with --dial to say something.")

    group_call.add_option("-u", "--url", action='store',
            metavar="URL of TWIML",
            dest="url", default=False,
            help="URL of TWIML to pass call with --call")

    group_call.add_option("-b", "--buy", action='store',
            dest="purchase", default=False,
            metavar="+12135551212",
            help="Buy a specific phone number listed with -x or -a")

    group_call.add_option("-a", "--area-code", action='store',
            dest="areacode", default=False,
            metavar="AREA CODE",
            help="Search for phone number to purchase by area code. " +
            "Use -b to purchase from these results.")

    group_call.add_option("-x", "--contains", action='store',
            dest="contains", default=False,
            help="Search for phone number to purchase by numbers " +
            "or letters it contains.")

    #Conferences
    group_conferences = optparse.OptionGroup(opt_parser,
            "Conference (voice) options",
            "These options can be used for voice conference calls.")

    group_conferences.add_option("-f", "--conference", action='store',
            metavar="+12135551212,+14155551212",
            help="Start conference with list of numbers to dial, " +
            "comma-separated.",
            dest="conference", default=False)

    group_conferences.add_option("-o", "--room",
            action='store',
            dest="room", default=False,
            help="Room to join for voice conference.")

    group_conferences.add_option("-e", "--conferences", action='store_true',
            dest="conferences", default=False,
            help="Show conferences in-progress.")

    group_conferences.add_option("-p", "--conference-participants",
            action='store_true',
            dest="participants", default=False,
            help="Show participants for all conferences in-progress.")

    #Reports
    group_reports = optparse.OptionGroup(opt_parser,
            "Reporting options",
            "List your Twilio phone numbers and information about each.")

    group_reports.add_option("-n", "--notifications", action='store_true',
            dest="notifications", default=False, help="Show notifications " +
            "from Twilio API (error messages and warnings).")

    group_reports.add_option("-r", "--numbers", action='store_true',
            dest="numbers", default=False, help="Show all my Twilio phone " +
            "numbers. Use -rv for detailed info on each number.")

    group_reports.add_option("--sid", action='store',
            dest="sid", default=False, help="Show log for given SID")

    #Applications
    group_applications = optparse.OptionGroup(opt_parser,
            "Applications",
            "Twilio Application information.")

    group_applications.add_option("--applications", action='store_true',
            dest="applications", default=False,
            help="Show all my Twilio Applications.")

    #Accounts
    group_accounts = optparse.OptionGroup(opt_parser,
            "Accounts options",
            "Twilio account and sub-account management")

    group_accounts.add_option("--list-accounts", action='store_true',
            dest="list_accounts",
            default=False,
            help="List all Twilio accounts and sub-accounts.")

    group_accounts.add_option("--create-sub-account", action='store',
            dest="create_subaccount",
            metavar="NAME",
            default=False,
            help="Create sub-account named 'NAME'")

    group_accounts.add_option("--rename-sub-account", action='store',
            dest="rename_account",
            metavar="NAME",
            default=False,
            help="Rename account or sub-account using 'NAME'")

    opt_parser.add_option_group(group_common)
    opt_parser.add_option_group(group_call)
    opt_parser.add_option_group(group_conferences)
    opt_parser.add_option_group(group_sms)
    opt_parser.add_option_group(group_reports)
    opt_parser.add_option_group(group_applications)
    opt_parser.add_option_group(group_accounts)
    return opt_parser


def main():
    """
    Let's do it.
    """
    my_twerp = Twerp()
    return my_twerp.run()

if __name__ == "__main__":
    sys.exit(main())
