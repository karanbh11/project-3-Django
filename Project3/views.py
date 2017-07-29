from django.http import *
from django.shortcuts import *
from Project3.settings import *
from app1.models import *
from Project3.forms import *
from django.contrib.auth.hashers import *
from imgurpython import ImgurClient
from django.core.mail import send_mail

def home(request):
	if request.method == "POST":
		form = signup(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user1 = user(firstname=firstname, lastname=lastname, username=username, password=make_password(password), email=email)
			user1.save()
			subject = 'Confirmation on joining Let\'s Share'
			message = 'Thanks for Joining Let\'s Share !!!!\n Welcome to the family \n Post and show the world who you are'
			from_email = EMAIL_HOST_USER
			to_email = [user1.email]
			
			send_mail(subject, message, from_email, to_email, fail_silently=True)
			
			return render(request, 'success.html', {'STATIC_URL':STATIC_URL})
	elif request.method == "GET":
		form = signup()
	return render(request, 'home.html', {'STATIC_URL':STATIC_URL, 'form':form})
	
def login_view(request):
	response_data = {}
	if request.method == "POST":
		form = log_in(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user1 = user.objects.filter(username=username).first()

			if user1:
				if check_password(password, user1.password):
					token = session_token(user=user1)
					token.create_token()
					token.save()
					response = redirect('/feed')
					response.set_cookie(key='session_token', value=token.session_token)
					return response
				else:
					response_data['message'] = 'Incorrect Password or Username! Please try again!'
			else:
				response_data['message'] = 'Incorrect Password or Username! Please try again!'
	elif request.method == 'GET':
		form = log_in()

	response_data['form'] = form
	response_data['STATIC_URL'] = STATIC_URL
	return render(request, 'log_in.html', response_data)


	
#For validating the session
def check_validation(request):
	if request.COOKIES.get('session_token'):
		session = session_token.objects.filter(session_token=request.COOKIES.get('session_token')).first()
		if session:
			return session.user
	else:
		return None

		
def post_view(request):
	user = check_validation(request)
	if user:
		if request.method == 'POST':
			form = post_form(request.POST, request.FILES)
			if form.is_valid():
				image = form.cleaned_data.get('image')
				caption = form.cleaned_data.get('caption')
				post1 = post(user=user, image=image, caption=caption)
				post1.save()
				path = str(post1.image.url)
				client = ImgurClient('14ffa56696f426a', 'd924dc264aee194c27c9f92eb19ba1c01f0b1d9b')
				post1.image_url = client.upload_from_path(path, config=None, anon=True)['link']
				post1.save()
				return redirect('/feed/')
		else:
			form = post_form()
		return render(request, 'post.html', {'form':form, 'STATIC_URL':STATIC_URL})
	else:
		return redirect('/log/')
	

def feed(request):
	user = check_validation(request)
	if user:
		posts = post.objects.all().order_by('created_on')
		
		for post1 in posts:
			existing_like = LikeModel.objects.filter(post=post1, user=user).first()
			if existing_like:
				post1.has_liked = True
			for comment in post1.comments:
				com_like = comment_like_model.objects.filter(user=user, comment=comment)
				if com_like:
					comment.c_like = True
		return render(request, 'feed.html', {'posts':posts, 'STATIC_URL':STATIC_URL})
	else:
		return redirect('/log/')
		
def like(request):
	user = check_validation(request)
	if user and request.method == 'POST':
		form = like_form(request.POST)
		if form.is_valid():
			post_id = form.cleaned_data.get('post').id
			existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
			if not existing_like:
				LikeModel.objects.create(post_id=post_id, user=user)
				poster = post.objects.filter(id=post_id).first()
				subject = 'Your photo was liked'
				message = 'Your photo was liked by ' + user.username
				from_email = EMAIL_HOST_USER
				to_email = [poster.user.email]
			
				send_mail(subject, message, from_email, to_email, fail_silently=True)
			else:
				existing_like.delete()
				poster = post.objects.filter(id=post_id).first()
				subject = 'Your photo was unliked'
				message = 'Your photo was unliked by ' + user.username
				from_email = EMAIL_HOST_USER
				to_email = [poster.user.email]
			
				send_mail(subject, message, from_email, to_email, fail_silently=True)
			return redirect('/feed/')
	else:
		return redirect('/login/')
		
def comment(request):
	user = check_validation(request)
	if user and request.method == 'POST':
		form = comment_form(request.POST)
		if form.is_valid():
			post_id = form.cleaned_data.get('post').id
			temp = post.objects.filter(id=post_id).first()
			comment_text = form.cleaned_data.get('comment_text')
			comment = CommentModel.objects.create(user=user, post=temp, comment_text=comment_text)
			comment.save()
			poster = post.objects.filter(id=post_id).first()
			subject = 'A comment on your photo'
			message = str(user.username) + ' commented on you photo..\n\n HE SAYS: ' + comment_text
			from_email = EMAIL_HOST_USER
			to_email = [poster.user.email]
			
			send_mail(subject, message, from_email, to_email, fail_silently=True)
			
			return redirect('/feed/')
		else:
			return redirect('/feed/')
	else:
		return redirect('/login')

	
def log_out(request):
	if request.COOKIES.get('session_token'):
		session = session_token.objects.filter(session_token=request.COOKIES.get('session_token'))
		session.delete()
	return render(request, 'log_out.html', {'STATIC_URL':STATIC_URL})
	
def comment_like(request):
	user = check_validation(request)
	if user and request.method == 'POST':
		form = comment_like_form(request.POST)
		if form.is_valid():
			comment_id = form.cleaned_data.get('comment').id
			comment = CommentModel.objects.filter(id=comment_id).first()
			existing_like = comment_like_model.objects.filter(user=user, comment=comment).first()
			if not existing_like:
				comment_like_model.objects.create(user=user, comment=comment)
			else:
				existing_like.delete()
			return redirect('/feed/')
		else:
			return HttpResponse("form data is invalid.")
	else:
		return redirect('/login/')
		
def search(request):
	if "q" in request.GET:
		q = request.GET["q"]
		posts = post.objects.filter(user__username__icontains=q)
		return render(request, 'feed.html', {"posts":posts, "query":q, 'STATIC_URL':STATIC_URL})
	return render(request, "feed.html")