
"""

twiliolib.py
============

Desc: Send and receive SMS or make calls via Twilio REST API

Author: Rob Cakebread <cakebread @ gmail*com>

License : BSD

"""

__docformat__ = 'restructuredtext'


import os
import sys
import logging
from configobj import ConfigObj
from urllib import quote_plus

from httplib2 import ServerNotFoundError
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from twilio.rest.resources import Call
from clint.textui import colored, puts, indent
try:
    import simplejson as json
except ImportError:
    import json


twerp_config = os.path.join(os.path.expanduser("~"), '.twerprc')

if not os.path.exists(twerp_config):
    print """Create ~/.twerprc with:

    AUTH_TOKEN = lkasjdfkljsl
    ACCOUNT_SID = iowjroiwjeroij
    CALLER_ID = +12135551212
    """
    sys.exit(1)
config = ConfigObj(twerp_config)

AUTH_TOKEN = config['AUTH_TOKEN']
ACCOUNT_SID = config['ACCOUNT_SID']
CALLER_ID = config['CALLER_ID']

URL_CONFERENCE_TWIML = '''http://tinyurl.com/6vyxerr'''


#From TwilioRestClient.phone_numbers.
NUMBER_IDS = ['account_sid', 'api_version', 'auth', 'base_uri', 'capabilities',
            'date_created', 'date_updated', 'friendly_name', 'id_key',  'name',
            'phone_number', 'sid', 'sms_application_sid',
            'sms_fallback_method', 'sms_fallback_url', 'sms_method', 'sms_url',
            'status_callback', 'status_callback_method', 'subresources', 'uri',
            'voice_application_sid', 'voice_caller_id_lookup',
            'voice_fallback_method', 'voice_fallback_url', 'voice_method',
            'voice_url']


class RestClient(object):

    '''Holds client for REST connection'''

    def __init__(self, connect=True):
        self.logger = logging.getLogger("twerp")
        if connect:
            self.connect()

    def connect(self):
        '''Make a REST client connection to twilio'''
        self.client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    def rename_account(self, account_name, verbose=False):
        '''Create Twilio sub-account'''
        try:
            account = self.client.accounts.get(ACCOUNT_SID)
            account.update(friendly_name=account_name)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

    def list_accounts(self):
        '''List Twilio account and sub-accounts'''
        try:
            accounts = self.client.accounts.list()
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            print e.msg
            return 1
        for account in accounts:
            print account.friendly_name
            print account.sid
            print
        #print dir(account)

    def create_subaccount(self, account_name, verbose=False):
        '''Create Twilio sub-account'''
        try:
            apps = self.client.accounts.create(account_name)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

    def list_applications(self, verbose=False):
        '''Print error messages and warnings from Twilio'''
        try:
            apps = self.client.applications.list()
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for app in apps:
            print app.friendly_name
            print "\tSMS URL: %s" % app.sms_url
            print "\tVoice URL: %s" % app.voice_url
            print "=" * 79
            print

    def notifications(self, verbose=False):
        '''Print error messages and warnings from Twilio'''
        try:
            notes = self.client.notifications.list()
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

        notes.reverse()

        for notification in notes:
            print "=="
            print notification.date_created
            print notification.call_sid
            print "Error code: %s" % notification.error_code
            print "Error msg: %s" % notification.message_text
            print "Request URL: %s" % notification.request_url
            print "Error: %s" % notification.log
            if verbose:
                print notification.more_info
            print

    def list_conference_participants(self):
        """List all conferences"""
        try:
            conferences = self.client.conferences.list(status="in-progress")
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for conference in conferences:
            print conference.status
            print conference.date_created
            print conference.date_updated
            print conference.friendly_name
            print '[' + conference.sid[0:7] + '...]'
            print '=' * 79
            print

    def list_conferences(self):
        """List all conferences"""
        try:
            conferences = self.client.conferences.list(status="in-progress")
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for conference in conferences:
            print conference.status
            print conference.date_created
            print conference.date_updated
            print conference.friendly_name
            print '[' + conference.sid[0:7] + '...]'
            print '=' * 79
            print
            for participant in conference.participants.list():
                print participant.sid

    def sid_call(self, sid):
        """Print results for given SID"""
        try:
            call = self.client.calls.get(sid)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

        print 'date: %s' % call.date_created
        print 'from: %s' % call.from_
        print 'to: %s' % call.to
        print 'status: %s' % call.status
        print 'direction: %s' % call.direction
        print

    def purchase_number(self, number):
        """Purchase phone number"""
        try:
            number = self.client.phone_numbers.purchase(number)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

    def numbers_contain_areacode(self, area_code, contains):
        """Print numbers available for purchase"""
        try:
            numbers = self.client.phone_numbers.search(
                    area_code=area_code,
                    contains=contains)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for number in numbers:
            print number.phone_number
            print "Zip code: %s" % number.postal_code
            print "Region: %s" % number.region
            print "=" * 15
            print

    def numbers_contain(self, contains):
        """Print numbers available for purchase"""
        try:
            numbers = self.client.phone_numbers.search(contains=contains)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for number in numbers:
            print number.phone_number
            print "Zip code: %s" % number.postal_code
            print "Region: %s" % number.region
            print "=" * 15
            print

    def search_numbers(self, area_code):
        """Print numbers available for purchase"""
        try:
            numbers = self.client.phone_numbers.search(area_code=area_code)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1
        for number in numbers:
            print number.phone_number
            print "Zip code: %s" % number.postal_code
            print "Region: %s" % number.region
            print "=" * 15
            print

    def get_sms_sid(self, sid):
        """Print results for given SID"""
        try:
            sms = self.client.sms.messages.get(sid)
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

        print('date: %s' % sms.date_sent)
        print 'from: %s' % sms.from_
        print 'to: %s' % sms.to
        print 'status: %s' % sms.status
        print 'body: %s' % sms.body
        print

    def hangup(self, sid):
        '''Hangup a call by SID'''
        try:
            self.client.calls.hangup(sid)
            print "Call hung up."
            print
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            print msg["message"]
            return 1

    def hangup_all_calls(self):
        '''Call a URL/Twimlet'''
        try:
            calls = self.client.calls.list(status=Call.IN_PROGRESS)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        self.logger.info("Checking for calls in progress...")
        for c in calls:
            print "Hung up IN_PROGRESS SID: %s  From:%s" % (c.sid, c.from_)
            c.hangup()
        try:
            calls = self.client.calls.list(status=Call.RINGING)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        self.logger.info("Checking for calls that are ringing...")
        for c in calls:
            print "Hung up RINGING SID: %s  From:%s" % (c.sid, c.from_)
            c.hangup()

        self.logger.info("Checking for calls that are queued...")
        try:
            calls = self.client.calls.list(status=Call.QUEUED)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        for c in calls:
            print "Hung up QUEUED SID: %s  From:%s" % (c.sid, c.from_)
            c.hangup()
        print

    def list_calls(self):
        '''List calls IN_PROGRESS, RINGING, or QUEUED'''
        try:
            calls = self.client.calls.list(status=Call.IN_PROGRESS)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        for c in calls:
            print "SID: %s" % c.sid
            print "From: %s" % c.from_
            #print "Answered by: %s" % c.answered_by
            #This always shows None, maybe we can't get till call ends
            print "Status: %s" % c.status
            print "Direction: %s" % c.direction
            print "Start: %s" % c.start_time

        try:
            calls = self.client.calls.list(status=Call.RINGING)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        for c in calls:
            print "Ringing: %s" % c.sid

        try:
            calls = self.client.calls.list(status=Call.QUEUED)
        except TwilioRestException, e:
            msg = json.loads(e.msg)
            #print msg["message"]
            self.logger.error(msg)
            return 1

        for c in calls:
            print "Queued: %s" % c.sid

    def create_conference(self, recipients, room, verbose=False,
            callerid=CALLER_ID):
        """
        callerid: string
        recipients: list of strings representing each phone number
        """

        if callerid is None:
            callerid = CALLER_ID

        my_url = URL_CONFERENCE_TWIML.replace('ROOM_NAME', room)
        self.logger.debug(my_url)
        for phone in recipients:
            self.logger.info("Placing call to: %s" % phone)
            try:
                call = self.client.calls.create(to=phone,
                        from_=callerid, url=my_url)
            except ServerNotFoundError, e:
                self.logger.error(e)
                return
            except TwilioRestException, e:
                self.logger.error(e)
                return

            self.logger.info("Status: %s" % call.status)
            self.logger.debug("SID: %s" % call.sid)
        return call.sid

    def call_numbers(self, recipients, verbose=False, callerid=CALLER_ID,
            url=None, say=None):
        """
        callerid: string
        recipients: list of strings representing each phone number
        """

        if callerid is None:
            callerid = CALLER_ID

        if say:
            url = '''http://twimlets.com/message?Message%5B0%5D='''
            text = quote_plus(say)
            url = '%s%s' % (url, text)
        for phone in recipients:
            self.logger.info("Placing call to: %s" % phone)
            try:
                call = self.client.calls.create(to=phone,
                        from_=callerid, url=url)
            except ServerNotFoundError, e:
                self.logger.error(e)
                return None
            except TwilioRestException, e:
                self.logger.error(e)
                return None

            self.logger.info("Status: %s" % call.status)
            self.logger.info("SID: %s" % call.sid)
        return call.sid

    def send_sms(self, recipients, message, verbose=False, callerid=CALLER_ID):
        """
        callerid: string
        recipients: list of strings representing each phone number
        message: Text to send via SMS"""

        for phone in recipients:
            print("PHONE", phone)
            try:
                message = self.client.sms.messages.create(to=phone,
                        from_=callerid,
                        body=message)
            except ServerNotFoundError, e:
                print e
                return 1
            except TwilioRestException, e:
                print e
                return 1
            if verbose:
                print("Status: %s" % message.status)
                print("SID: %s" % message.sid)
                print("From: %s" % message.from_)

    def list_numbers(self, verbose=False):
        """List all my Twilio numbers"""
        try:
            for number in self.client.phone_numbers.iter():
                puts('%s [%s]' % (number.phone_number, number.friendly_name))
                if verbose:
                    with indent(4, quote=colored.blue(' >')):
                        for id in NUMBER_IDS:
                            puts("%s: %s" % (colored.green(id),
                                getattr(number,
                                    NUMBER_IDS[NUMBER_IDS.index(id)])))

        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1

    def list_sms(self):
        """
        Retrieve list of all sms messages

        TODO: Add filtering for from, to and date
        """

        try:
            messages = self.client.sms.messages.list()
        except ServerNotFoundError, e:
            self.logger.error(e)
            return 1
        except TwilioRestException, e:
            print e
            return 1
        messages.reverse()
        for message in messages:
            print "%s t:%s f:%s sid:%s\n\t%s" % (message.date_sent, message.to,
                message.from_, message.sid, message.body)
