from django.forms import Form, PasswordInput, CharField, BooleanField

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
    remember_me = BooleanField(required=False, initial=True)


class RegistrationForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
    remember_me = BooleanField(required=False, initial=True)
