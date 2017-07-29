# Importing required files
from django import forms
from django.forms import ModelForm
from app1.models import *


# Forms defined for various purposes. Names suggest their use
class signup(forms.ModelForm):
	class Meta:
		model = user
		fields = ['firstname', 'lastname', 'username', 'email', 'password']
		
class log_in(forms.ModelForm):
	class Meta:
		model = user
		fields = ['username', 'password']
		
class post_form(forms.ModelForm):
	class Meta:
		model = post
		fields = ['image', 'caption']

class like_form(forms.ModelForm):
	class Meta:
		model = LikeModel
		fields = ['post']
		
class comment_form(forms.ModelForm):
	class Meta:
		model = CommentModel
		fields = ['comment_text', 'post']
		
class comment_like_form(forms.ModelForm):
	class Meta:
		model = comment_like_model
		fields = ['comment']