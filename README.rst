README
======

twerp version 0.0.5

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



Usage::
=======

    Usage: twerp [options]

    Options:
      -h, --help            show this help message and exit
      --version             Show twerp version and exit.
      -v, --verbose         Show more output stuff.
      --debug               Show debugging information.
      -q, --quiet           Show less output.

      Common options:
        These options can be used for both SMS and voice calls.

        -c CALLERID, --callerid=CALLERID
                            Phone number you are calling from or texting from.
        -i, --interactive   Go into interactive command-line mode after dialing
                            (voice or conferences).

      Voice call options:
        Place phone calls, execute TWIML.

        -d +12135551212,+14155551212, --dial=+12135551212,+14155551212
                            List of numbers to dial, comma-separated.
        -y Say something., --say=Say something.
                            Use with --dial to say something.
        -u URL of TWIML, --url=URL of TWIML
                            URL of TWIML to pass call with --call
        -b +12135551212, --buy=+12135551212
                            Buy a specific phone number listed with -x or -a
        -a AREA CODE, --area-code=AREA CODE
                            Search for phone number to purchase by area code. Use
                            -b to purchase from these results.

        -x CONTAINS, --contains=CONTAINS
                            Search for phone number to purchase by numbers or
                            letters it contains.

      Conference (voice) options:
        These options can be used for voice conference calls.

        -f +12135551212,+14155551212, --conference=+12135551212,+14155551212
                            Start conference with list of numbers to dial, comma-
                            separated.

        -o ROOM, --room=ROOM
                            Room to join for voice conference.
        -e, --conferences   Show conferences in-progress.
        -p, --conference-participants
                            Show participants for all conferences in-progress.

      SMS options:
        Send and reveive SMS text messages.

        -m <TXT MSG>, --message=<TXT MSG>
                            Send SMS text message

        -s +12135551212,+14155551212, --sms=+12135551212,+14155551212
                            Send SMS text message to list of numbers.

        -l, --list-sms      Show incoming SMS messages.

      Reporting options:
        List your Twilio phone numbers and information about each.

        -n, --notifications
                            Show notifications from Twilio API (error messages and
                            warnings).
        -r, --numbers       Show all my Twilio phone numbers. Use -Nv for detailed
                            info on each number.
        --sid=SID           Show log for given SID

      Applications:
        Twilio Application information.

        --applications      Show all my Twilio Applications.

Interactive Mode
================


The Prompt
----------

The prompt will have part of the SID if a call is in progress:

    twerp (CA3abc...) >>

If you hang up a call, for example, there will be no SID, so the prompt will look like this:

    twerp (...) >>


Interactive Mode Commands
-------------------------

 * list - List all calls in progress, ringing or queued
 * hangup - Hang up call associated with SID shown in prompt
 * nuke - Hang up all calls associated with account. ALL OF THEM!
 * forward <nnnnnnnnnn> - Redirect current call to another phone number
 * url <URL> - Redirect flow of call to TwiML at a URL
 * info [<SID>] - Show info for current SID or SID given
 * sid <SID> - Change the current SID associated with interactive-mode


TODO
----

See http://blog.cakebread.info/

