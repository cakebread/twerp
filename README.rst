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


    $ twerp -s 'this is a test' -r +12135551212

         Send SMS message


    $ twerp -L

         List all of your SMS messages (Be careful if you have zillions!)


    $ twerp -S nnnnnnnnnnnn

         Show details of SMS message by SID



TODO
----

See http://blog.cakebread.info/

