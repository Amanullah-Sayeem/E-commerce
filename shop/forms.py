from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def username_available(username):
    if not User.objects.filter(username=username).count():
        raise forms.ValidationError('username does not exist')


def email_exist(email):
    if User.objects.filter(email=email).count():
        raise forms.ValidationError('email already exists')


class BasicForm(forms.Form):
    def disable_field(self, field):
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]


def setup_field(field, placeholder=None):
    field.widget.attrs['class'] = 'form_control'
    if placeholder is not None:
        field.widget.attrs['placeholder'] = placeholder


class SignUpForm(BasicForm):
    username = forms.CharField(max_length=200,)
    setup_field(username, 'username')
    email = forms.EmailField(required=False, validators=[email_exist])
    setup_field(email, 'enter a email')
    password1 = forms.CharField(label='password', max_length=50, min_length=4, widget=forms.PasswordInput())
    setup_field(password1, 'password')
    password2 = forms.CharField(label='', widget=forms.PasswordInput())
    setup_field(password2, 'password again')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.mark_error('password2', ' password do not  match')

        return cleaned_data


class LogInForm(BasicForm):
    username = forms.CharField(max_length=20, validators=[username_available])
    setup_field(username, 'username')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LogInForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.mark_error('password', 'Incorrect Password')
        return cleaned_data
