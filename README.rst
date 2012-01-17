README
======

.. contents::


Installation
------------

pip install twerp



Configure twerp
---------------

~/.twerprc


ACCOUNT_SID=a902830980980980ff987yada

AUTH_TOKEN=98798asdfas9df87sadf987yada

CALLERID=+12135551212



Usage Examples
==============

    $ twerp -N

         List your Twilio phone numbers


    $ twerp -Nv

         List lots of details about each of your Twilio numbers:


    $ twerp -m 'this is a test' -s +12135551212

         Send SMS message to +12135551212

    $ twerp -c +12135551212 -u http://computer.net/TWIML

         Call +12135551212 and execute the TWIML at given URL

    $ twerp -c +12135551212,+13235551212 -u http://twimlets.com/conference?Music=rock

         Call two numbers and put them in a conference room. First one gets rock music till another caller joins.


    $ twerp -l

         List all of your SMS messages (Be careful if you have zillions, filtering coming soon)


    $ twerp -S nnnnnnnnnnnn

         Show details of SMS message by SID


    $ twerp -i --dial +13235551212 -u http://twimlets.com/conference?Music=rock
         Go into interactive command-line mode after calling number.


Interactive Mode
================


The Prompt
----------

The prompt will have part of the SID if a call is in progress:

    twerp (CA3...ab) >>

If you hang up a call, for example, there will be no SID, so the prompt will look like this:

    twerp (...) >>


Interactive Mode Commands
-------------------------

list - List all calls in progress, ringing or queued
hangup - Hang up call associated with SID shown in prompt
nuke - Hang up all calls associated with account. ALL OF THEM!
forward - Forward call to another phone number
url - Redirect flow of call to TwiML at a URL
info - Show info for current SID or SID given
sid - Change the current SID associated with interactive-mode


TODO
----

See http://blog.cakebread.info/

