from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, FormView
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
from .forms import RegisterForm, LoginForm, PhoneVerificationForm
from .models import User

class IndexView(TemplateView):
    template_name = 'index.html'

class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                        The verification code is valid for 10 minutes."
    success_url = '/verify'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        print(self.request.POST['username'])
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        response = send_verfication_code(user)
        data = json.loads(response.text)

        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect('/dashboard')

        print(response.status_code, response.reason)
        print(response.text)
        return super().form_valid(form)


class PhoneVerificationView(SuccessMessageMixin, FormView):
    template_name = 'phone_confirm.html'
    form_class = PhoneVerificationForm
    success_message = "Congrats! you just verified your phone number!"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.phone_number_verified:
            messages.add_message(self.request, messages.INFO,
                                "User already Verified")
            return redirect('/dashboard')
        else:
            return super().dispatch(
                request, *args, **kwargs)


    def form_valid(self, form):
        one_time_password = self.request.POST['one_time_password']
        user = self.request.user
        response = verify_sent_code(one_time_password, user)
        print(response.status_code, response.reason)
        print(response.text)
        data = json.loads(response.text)

        if data['success'] == True:
            user.phone_number_verified = True
            user.save()
            messages.add_message(self.request, messages.INFO,
                         "User phone number verified!")
            return redirect('/dashboard')

        elif data['success'] == False:
            print("false")
            messages.add_message(self.request, messages.ERROR,
                         "User already verified!")
            return redirect('/dashboard')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO,
                                "User already logged in")
            return redirect('/dashboard')
        else:
            return super().dispatch(
                request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        print(user, username, password)
        if user is not None:
            login(self.request, user)
            return redirect('/dashboard')
        else:
            return redirect('/login')


@method_decorator(login_required(login_url="/login/"), name='dispatch')
class DashboardView(SuccessMessageMixin, View):
    template_name = 'dashboard.html'

    def get(self, request):
        context = {
                'user': request.user,
        }
        return render(self.request, self.template_name, context)
