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
--------------

    $ twerp -N

         List your Twilio phone numbers


    $ twerp -Nv

         List lots of details about each of your Twilio numbers:


    $ twerp -m 'this is a test' -s +12135551212

         Send SMS message to +12135551212

    $ twerp -c +12135551212 -u http://computer.net/TWIML
         Call +12135551212 and execute the TWIML at given URL

    $ twerp -l

         List all of your SMS messages (Be careful if you have zillions, filtering coming soon)


    $ twerp -S nnnnnnnnnnnn

         Show details of SMS message by SID



TODO
----

See http://blog.cakebread.info/

