from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('7A53456A6A4478784B567837775A5752665233655A66726D765050315353593468645370784157495354513D')
        params = {
            'sender' : '1000596446',
            'receptor' : 'phone_number',
            'message' : f'{code}کد تایید شما',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

class UserPassesTest(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated 
    # and self.request.user.is_admin











