from django.db import models

# Create your models here.

class user(models.Model):
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30)
	username = models.CharField(max_length=20)
	email = models.EmailField()
	password = models.CharField(max_length=30)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)