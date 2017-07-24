from django import forms
from app1.models import user

class signup(forms.ModelForm):
	class meta:
		model = user
		fields = ['firstname', 'lastname', 'username', 'email', 'password']
		
class log_in(forms.ModelForm):
	class meta:
		model = user
		fields = ['username', 'password']