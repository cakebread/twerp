
Welcome to twerp
================

twerp is a command-line utility for making phone calls, conference calls, and sending and receiving SMS text messages with Twilio's API. It is written in Python.

Example Usage
=============

    $ twerp -N

         List your Twilio phone numbers


    $ twerp -Nv

         List lots of details about each of your Twilio numbers:


    $ twerp -m 'this is a test' -s +12135551212

         Send SMS message to +12135551212

    $ twerp -d +12135551212 -u http://computer.net/TwiML

         Call +12135551212 and execute the TWIML at given URL

    $ twerp -i -d +12135551212 -u http://computer.net/TwiML

         Call +12135551212 and execute the TWIML at given URL, then go interactive command-line mode.
         You can then modify the call live with different verbs such as 'url <URL' to re-route calls.

    $ twerp -d +12135551212,+13235551212 -u http://twimlets.com/conference?Music=rock

         Call two numbers and put them in a conference room. First one gets rock music till another caller joins.


    $ twerp -l

         List all of your SMS messages (Be careful if you have zillions, filtering coming soon)


    $ twerp -S nnnnnnnnnnnn

         Show details of SMS message by SID


Articles
========

* http://blog.cakebread.info/2012/01/twerp-twilio-command-line-client-for.html


Credits
========
 
* Rob Cakebread - Author



