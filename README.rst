Twerp README
============


Configure twerp:

~/.twerprc


ACCOUNT_SID=a902830980980980ff987yada
AUTH_TOKEN=98798asdfas9df87sadf987yada
CALLERID=+12135551212


Usage Examples:


List your Twilio phone numbers:

twerp -N


List lots of details about each of your Twilio numbers:

twerp -Nv


Send SMS message:

twerp -s 'this is a test' -r +12135551212


List all your SMS messages (Careful if you have zillions!)

twerp -L


Show details of SMS message by SID

twerp -S nnnnnnnnnnnn


