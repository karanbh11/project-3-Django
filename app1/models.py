from django.db import models
import uuid

# Create your models here.
# The names of the models suggest their use
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
	last_request_on = models.DateTimeField(auto_now=True)
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
	
	# This counts the no. of likes on an image
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
	
	# It counts the no. of upvotes on a comment
	@property
	def comment_like_count(self):
		return len(comment_like_model.objects.filter(comment=self))
	
class comment_like_model(models.Model):
	user = models.ForeignKey(user)
	comment = models.ForeignKey(CommentModel)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

