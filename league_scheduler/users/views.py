from django.shortcuts import render
from django.conf import settings
from django.dispatch import receiver
from authlib.integrations.django_client import OAuth, token_update
from django.http import HttpResponse
oauth = OAuth()
oauth.register(
    name='discord',
    client_id= settings.DISCORD_CLIENT_ID,
    client_secret= settings.DISCORD_CLIENT_SECRET,
    access_token_url='https://discord.com/api/oauth2/token',
    access_token_params=None,
    authorize_url='https://discord.com/api/oauth2/authorize',
    authorize_params=None,
    api_base_url='https://discord.com/api/v6/',
    client_kwargs={'scope':'identify'},
    #client_kwargs={'scope': 'user:email'},
)


def login(request):
    discord = oauth.create_client('discord')
    redirect_uri = request.build_absolute_uri('/users/authorize')
    #redirect_uri = "http://localhost:8000/users/authorize"
    return discord.authorize_redirect(request, redirect_uri)

def authorize(request):
    token = oauth.discord.authorize_access_token(request)
    #token is:
    #{'access_token': 'duSE8Fv9YNYXChrhJs1Y9tdZe0HZ38', 'expires_in': 604800, 'refresh_token': 'i3PBK2PlUvOspmppEsNatpMCpEirEo', 'scope': 'identify', 'token_type': 'Bearer', 'expires_at': 1656704767}
    response = oauth.discord.get('users/@me', token=token)
    response.raise_for_status()
    profile = response.json()
    #profile is:
    #{'id': '194512118853271552', 'username': 'Fudly', 'avatar': '0d0d67f276cba0e61fd02572d6cf2126', 'avatar_decoration': None, 'discriminator': '7712', 'public_flags': 0, 'flags': 0, 'banner': None, 'banner_color': None, 'accent_color': None, 'locale': 'en-US', 'mfa_enabled': False}
    return HttpResponse("<p>%s</p><p> %s</p>"%(token, profile))

#I have no idea if I need this function or not. The Authlib documentation is awful.
@receiver(token_update)
def on_token_update(sender, name, token, refresh_token=None, access_token=None, **kwargs):
    if refresh_token:
        item = OAuth2Token.find(name=name, refresh_token=refresh_token)
    elif access_token:
        item = OAuth2Token.find(name=name, access_token=access_token)
    else:
        return

    # update old token
    item.access_token = token['access_token']
    item.refresh_token = token.get('refresh_token')
    item.expires_at = token['expires_at']
    item.save()
