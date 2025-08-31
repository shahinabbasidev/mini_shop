from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from account.forms import LoginForm


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
                form.add_error("phone","phone or password is incorrect")
        else:
            form.add_error("phone","phone or password is incorrect")

        return render(request, "account/sing_in.html", {'form': form})
