from contextlib import suppress

from asgiref.sync import sync_to_async

@sync_to_async
def get_session_data(request, key:str, default=None) -> str:
    return request.session.get(key, default)

@sync_to_async
def set_session(request, key:str, value):
    request.session[key] = value

@sync_to_async
def delete_session(request, key:str):
    with suppress(KeyError):
        del request.session[key]