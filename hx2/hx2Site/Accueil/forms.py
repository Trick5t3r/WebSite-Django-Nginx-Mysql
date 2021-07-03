from django.forms import CharField, Form, PasswordInput
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class UserForm(Form):
    identifiant = CharField(label='Name', required=True)
    password = CharField(label='Password', widget=PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        identifiantCourrant = cleaned_data.get("identifiant")
        passwordCourrant = cleaned_data.get("password")
        user = authenticate(username=identifiantCourrant, password=passwordCourrant)
        if user is None:
        	raise ValidationError("Authentication error: incorrect username or password")