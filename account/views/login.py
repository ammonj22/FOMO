from django import forms
from django.conf import settings
from django_mako_plus import view_function, jscontext, RedirectException
from datetime import datetime, timezone
from account import models as amod
import re
from django.contrib.auth import authenticate, login
from formlib import Formless
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
    print('<<<<<<<<<<', 'I did something')
    form = LoginForm(request)
    if form.is_valid():
        form.commit()

        return HttpResponseRedirect('/account/')

    return request.dmp_render('login.html', {
        'form' : form,
    })

class LoginForm(Formless):
    def init(self):
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password = self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')

        return self.cleaned_data

    def commit(self):
        login(self.request, self.user)
