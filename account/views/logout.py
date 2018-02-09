from django.conf import settings
from django_mako_plus import view_function, jscontext, RedirectException
from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
    logout(request)
    return HttpResponseRedirect('/account/index/')
