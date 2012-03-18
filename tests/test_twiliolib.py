

from httplib2 import ServerNotFoundError
from mock import Mock, MagicMock, patch
from twerp.twiliolib import RestClient


def test_send_sms():

    real = RestClient()
    #Normal call
    real.send_sms = Mock()
    real.send_sms(['+13233333333'], 'message', False, '+18183333333')


    


def test_send_sms_server_not_found():

    real = RestClient()
    real.send_sms = Mock(side_effect=ServerNotFoundError('Server not found, dude.')).return_value = 2



    


