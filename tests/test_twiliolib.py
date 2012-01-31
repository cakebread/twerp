
from mock import Mock
from twerp.twiliolib import send_sms, list_numbers


def test_send_sms():
    send_sms('12135551212', 'message', False, '12135551212')
    real = send_sms
    real.send_sms = Mock(return_value=0)
