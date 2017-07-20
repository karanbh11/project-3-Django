from django.http import *
from django.shortcuts import *

def home(request):
	return render(request, 'home.html')