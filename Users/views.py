import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
import json


# Create your views here.

def register(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    if request.POST.get('password1') is not None:
        if request.POST.get('password1') == request.POST.get('password2'):
            password = request.POST.get('password1')
            url = os.environ.get("URL", 'https://api.giftshare.xyz/login/register')
            url = "%s" % url
            body = {
                "username": username,
                "email": email,
                "password": password,
            }
            req = requests.post(url, json=body)
            print(req.content)
            print(req.status_code)
            if req.status_code == 200:
                request.session['email_session'] = email
                return redirect(verification)
    return render(request, 'registration_page.html')


def verification(request):
    email = str(request.session.get('email_session'))
    code = str(request.POST.get('code'))
    if email is not None and code is not None:
        url = os.environ.get("URL", 'https://api.giftshare.xyz/login/verifyaccount/' + email + "/" + code)
        url = "%s" % url
        req = requests.post(url)
        print("email:" + email)
        print(req.content)
        if req.status_code == 200:
            return redirect('login')
    return render(request, 'verification_page.html')


def login(request):
    if (request.session.get('email_session')) is not None:
        email = str(request.session.get('email_session'))
    else:
        email = str(request.POST.get('email'))
    print(email)
    password = str(request.POST.get('password'))
    if email and password is not None:
        url = os.environ.get("URL", 'https://api.giftshare.xyz/login/signin')
        url = "%s" % url
        body = {
            "email": email,
            "password": password,
        }
        req = requests.post(url, json=body)
        print("status code logowania: " + str(req.status_code))
        response = req.json()
        request.session['token_session'] = response.get('token')
        if req.status_code == 200:
            return HttpResponse("zalogowano")
    return render(request, 'login_page.html', {
        "email": email,
    })
