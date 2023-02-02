from django.contrib import admin
#import the model made
from .models import Post,UserProfile,Comment, Notification

admin.site.register(Post)
# this will make it so that you can visit it in the admin page

admin.site.register(UserProfile)
#access it in the admin panel

admin.site.register(Comment)
#access it in the admin panel

admin.site.register(Notification)
#access it in the admin panel