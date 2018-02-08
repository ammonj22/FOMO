from django import forms
from django.conf import settings
from django_mako_plus import view_function, jscontext, RedirectException
from datetime import datetime, timezone
from account import models as amod
import re
from django.contrib.auth import authenticate, login
from formlib import Formless

@view_function
def process_request(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            form.commit()

            raise RedirectException('/account/')
    else:
        form = LoginForm(request)

    context = {
        'form': form,
    }
    return request.dmp_render('index.html', context)

class LoginForm(Formless):
    def init(self):
        self.fields['email'] = forms.CharField(label='Email Address')
        self.fields['password'] = forms.CharField(label='Password', widget=forms.PasswordInput())
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password = self.password)
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')

        return self.cleaned_data

    def commit(self):
        login(self.request, self.user)
