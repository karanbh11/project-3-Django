from django import forms
from app1.models import *

class signup(forms.ModelForm):
	class meta:
		model = user
		fields = ['firstname', 'lastname', 'username', 'email', 'password']
		
class log_in(forms.ModelForm):
	class meta:
		model = user
		fields = ['username', 'password']
		
class post(forms.ModelForm):
	class Meta:
		model = post
		fields = ['image', 'caption']

class like(forms.ModelForm):
	class Meta:
		model = LikeModel
		fields = ['post']
		
class comment(forms.ModelForm):
	class Meta:
		model = CommentModel
		fields = ['comment_text', 'post']