import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from network.models import SNUser
from network.views import get_current_user
from .forms import VerifyForm, PhoneCreationForm
from . import verify


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    userinfo = request.session.get("user")['userinfo']
    userExists = False
    for snuser in SNUser.objects.all():
        if userinfo['nickname'] == snuser.nickname:
            userExists = True
            break
    if not userExists:
        SNUser.objects.create(nickname=userinfo['nickname'], mail=userinfo['email'])
        return redirect('/add_number')
    return redirect(request.build_absolute_uri(reverse("index")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def add_number(request):
    if request.method == 'POST':
        form = PhoneCreationForm(request.POST)
        if form.is_valid():
            user = get_current_user(request=request)
            user.phone_number = form.cleaned_data.get('phone')
            user.save()
            verify.send(form.cleaned_data.get('phone'))
            return redirect('/verify')
    else:
        form = PhoneCreationForm()
    return render(request, 'add_number.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            user = get_current_user(request=request)
            if verify.check(user.phone_number, code):
                user.verified = True
                user.save()
                return redirect('index')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})