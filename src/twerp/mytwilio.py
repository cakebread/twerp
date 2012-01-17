
"""

mytwilio.py
======

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

logger = logging.getLogger("twerp")
twerp_config = os.path.join(os.path.expanduser("~"), '.twerprc')

if not os.path.exists(twerp_config):
    print """Create ~/.twerprc with:

    AUTH_TOKEN = lkasjdfkljsl
    ACCOUNT_SID = iowjroiwjeroij
    CALLER_ID = +13235551212
    """
    sys.exit(1)
config = ConfigObj(twerp_config)

AUTH_TOKEN = config['AUTH_TOKEN']
ACCOUNT_SID = config['ACCOUNT_SID']
CALLER_ID = config['CALLER_ID']
MAX_LENGTH = 160

'''
These are for showing detailed info about your Twilio phone numbers. It uses
TwilioRestClient.phone_numbers. There are some I didn't cover because they
require making multiple API calls, I don't know what they do yet, or aren't
applicable.
'''
NUMBER_IDS = ['account_sid', 'api_version', 'auth', 'base_uri', 'capabilities',
            'date_created', 'date_updated', 'friendly_name', 'id_key',  'name',
            'phone_number', 'sid', 'sms_application_sid',
            'sms_fallback_method', 'sms_fallback_url', 'sms_method', 'sms_url',
            'status_callback', 'status_callback_method', 'subresources', 'uri',
            'voice_application_sid', 'voice_caller_id_lookup',
            'voice_fallback_method', 'voice_fallback_url', 'voice_method',
            'voice_url']


class FakeCall(object):
    '''For making --pretend calls'''
    def __init__(self):
        self.sid = "YOURSID"
        self.status = "in progress(test)"


def trim(text_msg):
    '''Text messages have a finite length'''
    return text_msg[0:MAX_LENGTH]


def notifications(verbose=False):
    '''Print error messages and warnings from Twilio'''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    notes = client.notifications.list()
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


def sid_call(sid):
    """Print results for given SID"""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    try:
        call = client.calls.get(sid)
    except ServerNotFoundError, e:
        logger.error(e)
        return 1
    except TwilioRestException, e:
        print e
        return 1

    print 'date: %s' % call.date_created
    print 'from: %s' % call.from_
    print 'to: %s' % call.to
    print 'status: %s' % call.status
    print 'direction: %s' % call.direction
    print


def get_sms_sid(sid):
    """Print results for given SID"""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    try:
        sms = client.sms.messages.get(sid)
    except ServerNotFoundError, e:
        logger.error(e)
        return 1
    except TwilioRestException, e:
        print e
        return 1

    print 'date: %s' % sms.date_sent
    print 'from: %s' % sms.from_
    print 'to: %s' % sms.to
    print 'status: %s' % sms.status
    print 'body: %s' % sms.body
    print


def hangup(sid):
    '''Hangup a call by SID'''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    try:
        client.calls.hangup(sid)
        print "Call hung up."
        print
    except TwilioRestException, e:
        logger.error(e)
        return 1


def call_url(sid, url):
    '''Call a URL/Twimlet'''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    try:
        return client.calls.route(sid, url, method="POST")
    except TwilioRestException, e:
        logger.error(e)
        return 1


def hangup_all_calls():
    '''Call a URL/Twimlet'''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    calls = client.calls.list(status=Call.IN_PROGRESS)
    for c in calls:
        print "Hung up IN_PROGRESS SID: %s  From:%s" % (c.sid, c.from_)
        c.hangup()
    calls = client.calls.list(status=Call.RINGING)
    for c in calls:
        print "Hung up RINGING SID: %s  From:%s" % (c.sid, c.from_)
        c.hangup()

    calls = client.calls.list(status=Call.QUEUED)
    for c in calls:
        print "Hung up QUEUED SID: %s  From:%s" % (c.sid, c.from_)
        c.hangup()
    print


def list_calls():
    '''List calls IN_PROGRESS, RINGING, or QUEUED'''
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    calls = client.calls.list(status=Call.IN_PROGRESS)
    for c in calls:
        print "SID: %s" % c.sid
        print "From: %s" % c.from_
        #print "Answered by: %s" % c.answered_by
        #This always shows None, maybe we can't get till call ends
        print "Status: %s" % c.status
        print "Direction: %s" % c.direction
        print "Start: %s" % c.start_time

    calls = client.calls.list(status=Call.RINGING)
    for c in calls:
        print "Ringing: %s" % c.sid

    calls = client.calls.list(status=Call.QUEUED)
    for c in calls:
        print "Queued: %s" % c.sid


def call_numbers(recipients, verbose=False, callerid=CALLER_ID, url=None,
        say=None):
    """
    callerid: string
    recipients: list of strings representing each phone number
    """

    if callerid is None:
        callerid = CALLER_ID

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    if say:
        #Let's hope this URL never goes away.
        url = '''http://twimlets.com/message?Message%5B0%5D='''
        text = quote_plus(say)
        url = '%s%s' % (url, text)
    for phone in recipients:
        logger.info("Placing call to: %s" % phone)
        try:
            call = client.calls.create(to=phone, from_=callerid, url=url)
        except ServerNotFoundError, e:
            logger.error(e)
            return None
        except TwilioRestException, e:
            logger.error(e)
            return None

        #call = FakeCall()
        logger.info("Status: %s" % call.status)
        logger.info("SID: %s" % call.sid)
    return call.sid


def send_sms(recipients, message, verbose=False, callerid=CALLER_ID):
    """
    callerid: string
    recipients: list of strings representing each phone number
    message: Text to send via SMS"""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    for phone in recipients:
        try:
            message = client.sms.messages.create(to=phone, from_=callerid,
                    body=message)
        except ServerNotFoundError, e:
            logger.error(e)
            return 1
        except TwilioRestException, e:
            logger.error(e)
            return 1
        if verbose:
            logger.info("Status: %s" % message.status)
            logger.info("SID: %s" % message.sid)
            logger.info("From: %s" % message.from_)


def list_numbers(verbose=False):
    """List all my Twilio numbers"""
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    try:
        for number in client.phone_numbers.iter():
            puts(number.friendly_name)
            if verbose:
                with indent(4, quote=colored.blue(' >')):
                    for id in NUMBER_IDS:
                        puts("%s: %s" % (colored.green(id),
                            getattr(number, NUMBER_IDS[NUMBER_IDS.index(id)])))

    except ServerNotFoundError, e:
        logger.error(e)
        return 1


def list_sms():
    """
    Retrieve list of all sms messages

    TODO: Add filtering for from, to and date
    """

    #from_ = CALLER_ID
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    try:
        messages = client.sms.messages.list()
    except ServerNotFoundError, e:
        logger.error(e)
        return 1
    except TwilioRestException, e:
        print e
        return 1
    messages.reverse()
    for message in messages:
        print "%s t:%s f:%s sid:%s\n\t%s" % (message.date_sent, message.to,
            message.from_, message.sid, message.body)
