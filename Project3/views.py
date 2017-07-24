from django.http import *
from django.shortcuts import *
from Project3.settings import STATIC_URL
from app1.models import user
from forms import signup
from django.contrib.auth.hashers import *

def home(request):
	if request.method == "POST":
		form = signup(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = user(firstname=firstname, lastname=lastname, username=username, password=make_password(password), email=email)
			user.save()
	elif request.method == "GET":
		form = signup()
	return render(request, 'home.html', {'STATIC_URL':STATIC_URL, 'form':form})
	
def log_in(request):
	if request.method == "POST":
		form = log_in(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = user.objects.filter(username=username).first()
			if user:
				# Authenticating the password
				if check_password(password, user.password):
					print('User is valid')
				else:
					print('User is invalid')
	elif request.method == "GET":
		form = log_in()
	return render(request, 'log_in.html', {'STATIC_URL':STATIC_URL, 'form':form})

