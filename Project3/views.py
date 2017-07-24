from django.http import *
from django.shortcuts import *
from Project3.settings import STATIC_URL
from app1.models import user
from Project3.forms import signup
from django.contrib.auth.hashers import *
from imgurpython import ImgurClient
from Project3.settings import BASE_DIR

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
					token = SessionToken(user=user)
					token.create_token()
					token.save()
					response = redirect('feed/')
					response.set_cookie(key='session_token', value=token.session_token)
					return response
				else:
					response_data['message'] = 'Incorrect Password! Please try again!'
	elif request.method == "GET":
		form = log_in()
	response_data['form'] = form
	return render(request, 'log_in.html', response_data, {'STATIC_URL':STATIC_URL})


	
#For validating the session
def check_validation(request):
	if request.COOKIES.get('session_token'):
		session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
		if session:
			return session.user
	else:
		return None

		
def post(request):
	user = check_validation(request)
	if user:
		if request.method == 'POST':
			form = PostForm(request.POST, request.FILES)
			if form.is_valid():
				image = form.cleaned_data.get('image')
				caption = form.cleaned_data.get('caption')
				post = post(user=user, image=image, caption=caption)
				post.save()
				path = str(BASE_DIR + post.image.url)
				client = ImgurClient(14ffa56696f426a, d924dc264aee194c27c9f92eb19ba1c01f0b1d9b)
				post.image_url = client.upload_from_path(path,anon=True)['link']
				post.save()
				return redirect('/feed/')
		else:
			form = postform()
		return render(request, 'post.html', {'form':form})
	else:
		return redirect('/login/')
	

def feed(request):
	return render(request, 'feed.html')
