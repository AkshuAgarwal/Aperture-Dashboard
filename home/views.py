from django.shortcuts import render, HttpResponse, redirect
import requests
import datetime

simple_invite_link = 'https://discord.com/api/oauth2/authorize?client_id=842032214761537589&permissions=8&scope=bot%20applications.commands'
login_invite_link = 'https://discord.com/api/oauth2/authorize?client_id=842032214761537589&permissions=8&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fcallback&response_type=code&scope=identify%20guilds%20bot%20applications.commands'
login_link = 'https://discord.com/api/oauth2/authorize?client_id=842032214761537589&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fcallback&response_type=code&scope=identify%20guilds'
support_link = 'https://www.google.com/'

API_ENDPOINT = 'https://discord.com/api'
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_ENDPOINT = "https://discord.com/api/users/@me"
CLIENT_ID = 842032214761537589
CLIENT_SECRET = 'vBZh85gzwO_GORlNZ686kw9F7g1qbX20'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'
SCOPE = 'identify%20guilds'


def exchange_code(code):
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    r = requests.post(TOKEN_URL, data=payload)
    r.raise_for_status()
    return r.json()

def use_refresh_token(refresh_token):
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    r = requests.post(TOKEN_URL, data=payload)
    r.raise_for_status()
    return r.json()

def get_user_data(access_token):
    url = USER_ENDPOINT
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url=url, headers=headers)
    r.raise_for_status()
    return r.json()


# Create your views here.
def index(request):
    try:
        time_cookie = request.COOKIES.get('logintime')
        if time_cookie is not None:
            login_time = datetime.datetime.strptime(request.COOKIES['logintime'], '%Y-%m-%d %H:%M:%S.%f')
            if (datetime.datetime.utcnow() - login_time).seconds < 604000:
                access_token = request.session['access_token']
                user_object = get_user_data(access_token)
                loggedin = True
                context = {"loggedin": loggedin, "user_data": user_object}
            else:
                loggedin = False
                context = {"loggedin": loggedin}
        else:
            loggedin = False
            context = {"loggedin": loggedin}
    except:
        loggedin = False
        context = {"loggedin": loggedin}
    return render(request, 'index.html', context)

def invite(request):
    try:
        time_cookie = request.COOKIES.get('logintime')
        if time_cookie is not None:
            login_time = datetime.datetime.strptime(request.COOKIES['logintime'], '%Y-%m-%d %H:%M:%S.%f')
            if (datetime.datetime.utcnow() - login_time).seconds < 604000:
                return redirect(simple_invite_link)
            else:
                return redirect(login_invite_link)
        else:
            return redirect(login_invite_link)
    except:
        return redirect(login_invite_link)

def support(request):
    return redirect(support_link)

def login(request):
    response = redirect(login_link)
    try:
        time_cookie = request.COOKIES.get('logintime')
        if time_cookie is not None:
            login_time = datetime.datetime.strptime(request.COOKIES['logintime'], '%Y-%m-%d %H:%M:%S.%f')
            if (datetime.datetime.utcnow() - login_time).seconds < 604000:
                access_token = request.session['access_token']
                return redirect('/dashboard')
            else:
                return response
        else:
            return response
    except:
        return response

def callback(request):
    response = redirect('/dashboard')
    time_cookie = request.COOKIES.get('logintime')
    try:
        try:
            if time_cookie is not None:
                refresh_token = request.session['refresh_token']
                refresh_token_response = use_refresh_token(refresh_token)
                access_token = request.session['access_token'] = refresh_token_response.get('access_token')
                request.session['refresh_token'] = refresh_token_response.get('refresh_token')
                response.set_cookie('logintime', datetime.datetime.utcnow())
            else:
                code = request.GET.get('code')
                access_token_response = exchange_code(code)
                request.session['access_token'] = access_token_response.get('access_token')
                request.session['refresh_token'] = access_token_response.get('refresh_token')
                response.set_cookie('logintime', datetime.datetime.utcnow())
        except:
            code = request.GET.get('code')
            access_token_response = exchange_code(code)
            request.session['access_token'] = access_token_response.get('access_token')
            request.session['refresh_token'] = access_token_response.get('refresh_token')
            response.set_cookie('logintime', datetime.datetime.utcnow())
    except:
        response = redirect('/')
    return response

def dashboard(request):
    return HttpResponse("op")

def logout(request):
    response = redirect('/')
    try:
        time_cookie = request.COOKIES.get('logintime')
        if time_cookie is not None:
            response.delete_cookie('logintime')
            try:
                request.session.pop('access_token')
            except:
                pass
            return response
        else:
            return response
    except:
        return response