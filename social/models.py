from tkinter.filedialog import SaveFileDialog
from django.db import models

#importing time zones and users
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#class post will inherit from models.Model
class Post(models.Model):

    #require 3 fields -> creating 3 variables

    #users types into this to create a post
    body = models.TextField()
    #always taking default value for date->leaving this blank so it always follows default Date and Time
    image = models.ManyToManyField('Image', blank=True)
    # for images
    

    created_on = models.DateTimeField(default=timezone.now)
    
    #finds user currently logged in and puts that in his field
    #models.CASCADE tells Django to delete the referenced object when the other object is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #foreign key for the user

    likes=models.ManyToManyField(User, blank=True,related_name='likes')
    dislikes=models.ManyToManyField(User, blank=True,related_name='dislikes')
    shared_body = models.TextField(blank=True, null=True)
    shared_on = models.DateTimeField(blank=True, null=True)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    tags = models.ManyToManyField('Tag', blank=True)


    def create_tags(self):
        for word in self.body.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    self.save()
                
        if self.shared_body:
            for word in self.shared_body.split():
                if (word[0] == '#'):
                    tag = Tag.objects.filter(name=word[1:]).first()
                    if tag:
                        self.tags.add(tag.pk)
                    else:
                        tag = Tag(name=word[1:])
                        tag.save()
                        self.tags.add(tag.pk)
                    self.save()
		   

    class Meta:
        ordering = ['-created_on', '-shared_on']

class Comment(models.Model):
    comment= models.TextField()
    created_on= models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)

    def create_tags(self):
        for word in self.comment.split():
            if (word[0] == '#'):
                tag = Tag.objects.get(name=word[1:])
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()
        
    


class UserProfile(models.Model):
    #creating a foreign key relation between user and userprofile model, one user can have one profile 
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True,blank=True)
    location= models.CharField(max_length=100,blank=True,null=True)
    #for the image field install -> pip install Pillow
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)

    followers=models.ManyToManyField(User,blank=True, related_name='followers')


    


#functions to create and decorate user profile when we register
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()




class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)


class Notification(models.Model):
	# 1 = Like, 2 = Comment, 3 = Follow, #4 = DM
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)

class Image(models.Model):
	image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

class Tag(models.Model):
	name = models.CharField(max_length=255)





