from django.db import models
import uuid

# Create your models here.

class user(models.Model):
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	username = models.CharField(max_length=20)
	email = models.EmailField()
	password = models.CharField(max_length=30)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

class session_token(models.Model):
	user = models.ForeignKey(user)
	session_token = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
	is_valid = models.BooleanField(default=True)
	def create_token(self):
		self.session_token = uuid.uuid4()
		  
class post(models.Model):
	user = models.ForeignKey(user)
	image = models.FileField(upload_to='user_images')
	image_url = models.CharField(max_length=255)
	caption = models.CharField(max_length=240)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	
	@property
	def like_count(self):
		return len(LikeModel.objects.filter(post=self))
	
	@property
	def comments(self):
		return CommentModel.objects.filter(post=self).order_by('-created_on')


class LikeModel(models.Model):
	user = models.ForeignKey(user)
	post = models.ForeignKey(post)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	
class CommentModel(models.Model):
	user = models.ForeignKey(user)
	post = models.ForeignKey(post)
	comment_text = models.CharField(max_length=400)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

