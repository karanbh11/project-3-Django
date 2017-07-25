from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(user)
admin.site.register(post)
admin.site.register(session_token)
admin.site.register(LikeModel)
admin.site.register(CommentModel)