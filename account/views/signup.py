from django import forms
from django.conf import settings
from django_mako_plus import view_function, jscontext, RedirectException
from datetime import datetime, timezone, date
from django.http import HttpResponseRedirect
from account import models as amod
import re
from django.contrib.auth import authenticate, login
from formlib import Formless

@view_function
def process_request(request):
    if request.method == 'POST':
        form = SignupForm(request, request.POST)
        if form.is_valid():
            form.commit()

            raise RedirectException('/account/')
    else:
        form = SignupForm(request)

    context = {
        'form': form,
    }
    return request.dmp_render('signup.html', context)


class SignupForm(Formless):
    def init(self):
        self.fields['firstName'] = forms.CharField(label='First Name')
        self.fields['lastName'] = forms.CharField(label='Last Name')
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zipcode'] = forms.CharField(label='Zipcode')
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['birthdate'] = forms.DateField(label='Birthday', help_text='(mm/dd/yyyy)')
        self.fields['password'] = forms.CharField(label='Password' , widget=forms.PasswordInput())
        self.fields['password2'] = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            u1 = amod.User.objects.get(email = email)

        except:
            return email

        raise forms.ValidationError('You have already signed up with this email.')

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password needs to be at least 8 characters long.')

        if re.search('\d', password) is None:
            raise forms.ValidationError('Password needs to have at least one number.')

        return password

    def clean(self):
        if self.errors:
            return self.cleaned_data
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError('Please ensure the passwords match.')

        return self.cleaned_data

    def commit(self):
        u1 = amod.User()
        u1.first_name = self.cleaned_data.get('firstName')
        u1.last_name = self.cleaned_data.get('lastName')
        u1.address = self.cleaned_data.get('address')
        u1.city = self.cleaned_data.get('city')
        u1.state = self.cleaned_data.get('state')
        u1.zipcode = self.cleaned_data.get('zipcode')
        u1.email = self.cleaned_data.get('email')
        u1.birthdate = self.cleaned_data.get('birthdate')
        u1.set_password(self.cleaned_data.get('password'))
        u1.save()
        self.user = authenticate(email=self.cleaned_data.get('email'), password = self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')
        login(self.request, self.user)

