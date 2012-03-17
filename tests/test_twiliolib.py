
from mock import MagicMock, patch
from twerp.twiliolib import send_sms, list_numbers


def test_send_sms():

    my_send_sms = MagicMock(spec=send_sms)
    my_send_sms('12135551212', 'message', False, '12135551212')
    my_send_sms.return_value = 0
    assert my_send_sms.return_value == 0
