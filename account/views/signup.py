from django import forms
from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.http import HttpResponseRedirect
#from formlib import Formless

@view_function
def process_request(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # once you get here, everything is clean data. Don't do more data changes.
            # you can no longer inform the user that we have a problem
            # do the work of the form
            # make the payment
            # create the user
            return HttpResponseRedirect('/')

    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return request.dmp_render('signup.html', context)


class SignupForm(forms.Form):
    firstName = forms.CharField(label='First Name')
    lastName = forms.CharField(label='Last Name')
    address = forms.CharField(label='Address')
    email = forms.EmailField(label='Email')
    age = forms.IntegerField(label='Age')
    password = forms.CharField(label='Password' ,widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            # don't allow the signup
            raise forms.ValidationError('You need to be at least 18')
        return age

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError('Please ensure the passwords match.')

        return self.cleaned_data
