from django.contrib.auth import authenticate, login , logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, reverse
from django.views import View
from account.forms import LoginForm, OtpLoginForm, CheckOtpForm
import ghasedak_sms
from random import randint
from account.models import Otp
from uuid import uuid4
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
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("username", "username or password is incorrect")
        else:
            form.add_error("username", "username or password is incorrect")

        return render(request, "account/sing_in.html", {'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, "account/otp_login.html", {"form": form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
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
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], code=randcode, token=token)
            print(randcode)

            return redirect(
                reverse("account:check_otp") + f"?token={token}"
            )

        return render(request, "account/otp_login.html", {"form": form})


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {"form": form})

    def post(self, request):
        token = request.GET.get("token")
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'],token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("/")
            else:
                form.add_error("phone", "code or phone is incorrect")

            return render(request, "account/check_otp.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")
