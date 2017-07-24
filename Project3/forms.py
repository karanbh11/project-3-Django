from django import forms
from app1.models import user

class signup(forms.ModelForm):
	class meta:
		model = user
		feilds = ['firstname', 'lastname', 'username', 'email', 'password']