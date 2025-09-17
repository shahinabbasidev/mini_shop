from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, reverse
from django.views import View
from account.forms import LoginForm, RegisterForm, CheckOtpForm
import ghasedak_sms
from random import randint

from account.models import Otp

User = get_user_model()
sms_api = ghasedak_sms.Ghasedak(
    api_key='b4e2e29d1fa3e5ef586788afa525fd985ad31e9fbb34ab6949f9bfa1d7275d30p8NBzWgemb78to57')


# def account_login(request):
#     return render(request,"account/sing_in.html",{})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/sing_in.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("phone", "phone or password is incorrect")
        else:
            form.add_error("phone", "phone or password is incorrect")

        return render(request, "account/sing_in.html", {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = (randint(1000, 9999))

            otp_command = ghasedak_sms.SendOtpInput(
                send_date=None,
                receptors=[
                    ghasedak_sms.SendOtpReceptorDto(
                        mobile=cd["phone"]
                    )
                ],
                template_name="minishop",
                inputs=[
                    ghasedak_sms.SendOtpInput.OtpInput(
                        param="Code",
                        value=randcode
                    )
                ],
                udh=False
            )
            response = sms_api.send_otp_sms(otp_command)
            print("Ghasedak Response:", response)
            Otp.objects.create(phone=cd["phone"], code=randcode)
            print(randcode)

            return redirect(
                reverse("account:check_otp") + f"?phone={cd['phone']}"
            )

        return render(request, "account/register.html", {"form": form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {"form": form})

    def post(self, request):
        phone = request.GET.get("phone")
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd["code"], phone=phone).exists():
                user = User.objects.create_user(phone=phone, password=None)
                login(request, user)
                return redirect("/")
            else:
                form.add_error("code", "code is not correct")

        return render(request, "account/check_otp.html", {"form": form})
