from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, LoginForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from datetime import timedelta
from datetime import datetime
import pytz
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .backends import PhoneNumberBackend
utc = pytz.UTC



class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code = random_code)
            # expire_time = new_otp.created + timedelta(minutes=2)
            # if datetime.now() == expire_time:
            #     new_otp.delete()
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                expire_time = code_instance.created + timedelta(minutes=2)
                if expire_time >= timezone.now():
                    User.objects.create_user(phone_number=user_session['phone_number'], email=user_session['email'],
                                         full_name = user_session['full_name'], password=user_session['password'])
                else:
                    code_instance.delete()
                    messages.error(request, "your code is expired!", 'danger')
                    return redirect('accounts:verify_code')

                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')   
        

class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')

class UserLoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if PhoneNumberBackend.authenticate(self, request, phone_number=cd['phone_number'], password=cd['password']):
                user = User.objects.get(phone_number=cd['phone_number'])
                random_code = random.randint(1000, 9999)
                send_otp_code(cd['phone_number'], random_code)
                OtpCode.objects.create(phone_number=cd['phone_number'], code = random_code)
                request.session['user_login_info'] = {
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'full_name': user.full_name,
                    'password': user.password,
                }
                messages.success(request, 'we sent you a code', 'success')
                return redirect('accounts:login-verify')
            else:
                messages.error(request, 'The phone number or password is not valid.', 'danger')
                return redirect('accounts:login')
        return render(request, self.template_name, {'form':form})


class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_login_info']
        user = User.objects.get(phone_number=user_session['phone_number'], email=user_session['email'], full_name=user_session['full_name'], password=user_session['password'])
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                expire_time = code_instance.created + timedelta(minutes=2)
                if expire_time >= timezone.now():
                    User.objects.get(phone_number=user_session['phone_number'], email=user_session['email'],
                                         full_name = user_session['full_name'], password=user_session['password'])
                else:
                    code_instance.delete()
                    messages.error(request, "your code is expired!", 'danger')
                    return redirect('accounts:login-verify')
                login(request, user)
                code_instance.delete()
                messages.success(request, 'you logged in.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:login-verify')
        return redirect('home:home')   
        

