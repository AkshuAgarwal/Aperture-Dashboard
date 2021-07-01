import os
import asyncio
import httpx
from dotenv import load_dotenv
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, HttpResponse

from django_utils import get_session_data, set_session, delete_session

load_dotenv('./.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_ENDPOINT = 'https://discord.com/api'
TOKEN_ENDPOINT = 'https://discord.com/api/oauth2/token'
USER_ENDPOINT = 'https://discord.com/api/users/@me'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'
SCOPE = 'identify%20email%20guilds'
OAUTH2_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fcallback&response_type=code&scope=identify%20email%20guilds'


def main(request):
    request.session.set_test_cookie()
    return redirect('home/')

@sync_to_async
def manage_test_cookie(request):
    if request.session.test_cookie_worked():
        # try:
        #     request.session.delete_test_cookie()
        # except:
        #     pass
        return True
    else:
        return False

async def index(request):
    if await manage_test_cookie(request) is False:
        return redirect('/cookiedisabled/')

    context = {
        'logged_in': False,
        'avatar': None
    }

    _access_token = await get_session_data(request, 'ACCESS_TOKEN')
    if _access_token:
        _expires_on = await get_session_data(request, 'EXPIRES_ON')
        _expires_on = datetime.strptime(_expires_on, '%Y-%m-%d %H:%M:%S.%f') if _expires_on else None

        if _expires_on:
            if (_expires_on - datetime.utcnow()).seconds > 43200:
                context['logged_in'] = True
                headers = {"Authorization": f"Bearer {_access_token}"}
                resp = httpx.get(USER_ENDPOINT, headers=headers)
                resp.raise_for_status()
                data = resp.json()

                if not data['avatar']:
                    context['avatar'] = f'https://cdm.discordapp.com/embed/avatars/{int(data["discriminator"]) % 5}.png'
                elif str(data['avatar']).startswith('a_'):
                    context['avatar'] = f'https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.gif'
                else:
                    context['avatar'] = f'https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.png'

    return render(request, 'home/index.html', context)

async def login(request):
    if await manage_test_cookie(request) is False:
        return redirect('/cookiedisabled/')

    _access_token = await get_session_data(request, 'ACCESS_TOKEN')
    if _access_token:
        _expires_on = await get_session_data(request, 'EXPIRES_ON')
        _expires_on = datetime.strptime(_expires_on, '%Y-%m-%d %H:%M:%S.%f') if _expires_on else None

        if _expires_on:
            if (_expires_on - datetime.utcnow()).seconds > 43200:
                return redirect('/dashboard/')

    _refresh_token = await get_session_data(request, 'REFRESH_TOKEN')
    if _refresh_token:
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token':_refresh_token
        }
        resp = httpx.post(TOKEN_ENDPOINT, data=data)
        resp.raise_for_status()
        _resp_content = resp.json()

        await set_session(request, 'ACCESS_TOKEN', _resp_content['access_token'])
        await set_session(request, 'EXPIRES_ON', datetime.utcnow() + timedelta(seconds=_resp_content['expires_in']))

        return redirect('/dashboard/')

    return redirect(OAUTH2_URL)

async def callback(request):
    _code = request.GET.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': _code,
        'redirect_uri': REDIRECT_URI
    }
    resp = httpx.post(TOKEN_ENDPOINT, data=data)
    resp.raise_for_status()
    _resp_content = resp.json()

    _expiry_time = datetime.utcnow() + timedelta(seconds=_resp_content['expires_in'])

    await set_session(request, 'ACCESS_TOKEN', _resp_content['access_token'])
    await set_session(request, 'EXPIRES_ON', _expiry_time.strftime('%Y-%m-%d %H:%M:%S.%f'))

    return redirect('/dashboard/')

async def logout(request):
    await delete_session(request, 'ACCESS_TOKEN')
    await delete_session(request, 'EXPIRES_ON')
    return redirect('/')

def noscript(request):
    return render(request, 'utils/noscript.html')

def cookiedisabled(request):
    return render(request, 'utils/cookiedisabled.html')