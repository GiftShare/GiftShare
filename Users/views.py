import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json


# Create your views here.

# https://api.giftshare.xyz/login/register <-- zapytanie POST, rejestracja
# w body zapytania musi być:
# {
#     "username": "tu wpisz nick",
#     "email": "tu mail",
#     "password": "tu haslo"
# }

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

# https://api.giftshare.xyz/login/verifyaccount/<adres email kogos kogo weryfikujesz>/<kod z maila> <-- zapytanie POST, weryfikuje konto


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

# https://api.giftshare.xyz/login/signin - post, oddaje ci token
# w body:
# {
#     "email": "email dajesz",
#     "password": "tu dajesz haslo"
# }


def login(request):
    if request.POST.get('email') is not None:
        email = str(request.POST.get('email'))
    else:
        email = " "
    password = str(request.POST.get('password'))
    if email is not None and password is not None:
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
        else:
            return HttpResponse(response.get('result'))
    return render(request, 'login_page.html', {
        "email": email,
    })


# https://api.giftshare.xyz/post/create - post, tworzy ci pomysl
# w body:
# {
#     "token": "tu dajesz token z logowania",
#     "category": "tu dajesz kategorie, aktualnie mozliwe kategoria i kategoria1",
#     "content": "tu content jest, 200 znakow maksymalnie"
# }


def createPost(request):
    title = request.GET.get('title')
    description = request.GET.get("description")
    category = request.GET.get('category')
    if title and description and category is not None:
        url = os.environ.get("URL", 'https://api.giftshare.xyz/post/create')
        url = "%s" % url
        body = {
            "token": request.session["token"],
            "description": description,
            "category": category,
        }
        req = requests.post(url, json=body)
    return render(request, 'create_post_page.html', {

    })



