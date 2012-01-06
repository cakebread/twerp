
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

from twilio.rest import TwilioRestClient
from clint.textui import colored, puts, indent

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


#These are for showing detailed info about your Twilio phone numbers It uses
#TwilioRestClient.phone_numbers. There are some I didn't cover because they
#require making multiple API calls, I don't know what they do yet, or aren't
#applicable. A big TODO:
NUMBER_IDS = ['account_sid', 'api_version', 'auth', 'base_uri', 'capabilities',
            'date_created', 'date_updated', 'friendly_name', 'id_key',  'name',
            'phone_number', 'sid', 'sms_application_sid',
            'sms_fallback_method', 'sms_fallback_url', 'sms_method', 'sms_url',
            'status_callback', 'status_callback_method', 'subresources', 'uri',
            'voice_application_sid', 'voice_caller_id_lookup',
            'voice_fallback_method', 'voice_fallback_url', 'voice_method',
            'voice_url']


def get_sms_sid(sid):
    """Print results for given SID"""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    sms = client.sms.messages.get(sid)
    print sms.date_sent
    print 'from:', sms.from_
    print 'to:', sms.to
    print 'status:', sms.status
    print 'body:', sms.body


def call_numbers(recipients, verbose=False, callerid=CALLER_ID, url=None):
    """
    callerid: string
    recipients: list of strings representing each phone number
    """
    if callerid is None:
        #No callerid set with -i, using CALLER_ID in ~/.twerprc"
        callerid=CALLER_ID

    #twimlet = 'http://twimlets.com/message?Message%5B0%5D=twerp%20calling.%20Hello!&'
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    for phone in recipients:
        call = client.calls.create(to=phone, from_=callerid, url=url)
        if verbose:
            print "Status:", call.status
            print "SID:", call.sid



def send_sms(recipients, message, verbose=False, callerid=CALLER_ID):
    """
    callerid: string
    recipients: list of strings representing each phone number
    message: Text to send via SMS"""

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    for phone in recipients:
        message = client.sms.messages.create(to=phone, from_=callerid,
                body=message)
        if verbose:
            print "Status:", message.status
            print "SID:", message.sid
            print "From:", message.from_


def list_numbers(verbose=False):
    """List all my Twilio numbers"""
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    for number in client.phone_numbers.iter():
        puts(number.friendly_name)
        if verbose:
            with indent(4, quote=colored.blue(' >')):
                for id in NUMBER_IDS:
                    puts("%s: %s" % (colored.green(id),
                        getattr(number, NUMBER_IDS[NUMBER_IDS.index(id)])))


def list_sms():
    """Retrieve list of all sms messages"""
    #from_ = CALLER_ID
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    messages = client.sms.messages.list()
    messages.reverse()
    for message in messages:
        print "%s t:%s f:%s sid:%s\n\t%s" % (message.date_sent, message.to,
            message.from_, message.sid, message.body)
