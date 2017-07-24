from django.http import *
from django.shortcuts import *
from Project3.settings import STATIC_URL

def home(request):
	return render(request, 'home.html', {'STATIC_URL':STATIC_URL})
	
def log_in(request):
	return render(request, 'log_in.html', {'STATIC_URL':STATIC_URL})

