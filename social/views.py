from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
#importing generic views class
from django.views import View
from .models import Post,Comment,UserProfile,ThreadModel,MessageModel, Notification , Image, Tag
#importing from forms
from .forms import PostForm, CommentForm,ThreadForm,MessageForm, ShareForm,ExploreForm
#importing django generic views -> different view classes
from django.views.generic.edit import UpdateView, DeleteView 

from django.contrib import messages

# from views we go to urls

#Listing all the views in our social feed -> importing from the generic View class

#templates are refernced in views


class PostListView(LoginRequiredMixin, View):
#creating a get method for any get requests that comes to this url

    #handling a get request
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        #ordering posts from earliest to latest

        #basically using filter - only allowing users to see posts of users they are following
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        )
        form = PostForm()
        share_form = ShareForm()
        #creating a form -> creating a variable form

        context = {
            #dictionary 
            'post_list': posts,
            'shareform': share_form,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)



    #handling a post request
    def post(self, request, *args, **kwargs):

        logged_in_user = request.user
        #once post is submitted -> back to the same page
        
        #ordering posts from earliest to latest
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        
        form = PostForm(request.POST,request.FILES)
        share_form = ShareForm()
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False) #new_post is just a new_post object
            new_post.author = request.user #gets the currently signed in user
            new_post.save() #saves new post in database

            new_post.create_tags()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        context = {
            'post_list' : posts,
            'shareform': share_form,
            'form' : form,    
        }
        return render(request, 'social/post_list.html',context) #context-> pass our context




#to go to comments of the post


class PostDetailView(LoginRequiredMixin,View):
    #need a get method for get requests and a post method for post requests
    def get(self, request, pk, *args, **kwargs):
        #pk is a variable called ok and passing it in our argument
        post = Post.objects.get(pk=pk)
        #we can find the post in Post.objects.get(pk=pk), whatever the pk value is
        
        form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context={
            'post' : post,
            'form' : form,
            'comments' : comments,
        }
        return render(request, 'social/post_detail.html', context)

    #post method
    def post(self, request, pk, *args, **kwargs):
        
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()

        #taking the Commentobject and saving it to the post
        #on every comment object has a post value, if that matches the post here
        #then we'll take our list and reverse it by created on

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)
        
        context={
            'post' : post,
            'form' : form,
            'comments' : comments,
        }
        return render(request, 'social/post_detail.html', context)




#Update a post
class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    #specify different attributes -> models, field, template name

    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    #redirect back to details page
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk':pk})

    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author

#Delete a post
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Post
    template_name = 'social/remove_post.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author


#Delete a comment
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Comment
    template_name = 'social/remove_comment.html'
    
    #redirect back 
    def get_success_url(self):
        pk=self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk':pk})
    
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author




class ProfileView(View):
    def get(self, request, pk, *args, **kwargs): #handle get request when we need to view the profile
        
        #get the profile info and posts

        #if the primary key matches pk -> grab profile object and save it in profile variable
        profile=UserProfile.objects.get(pk=pk)

        user=profile.user
        posts=Post.objects.filter(author=user)
        #going to the post object and filtering it 
        #with get we get 1 with filter we get more than 1
        #basically if the user that posted it is the same user whoserofile you're trying to access matches ->post should show up on the profile

        followers = profile.followers.all()
        #get all objects from ManyToMany field

        if len(followers)==0:
            is_following=False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following=False

        number_of_followers=len(followers)
        #total number of followers


        context={
            'user':user,
            'profile': profile,
            'posts':posts,
            'number_of_followers' : number_of_followers,
            'is_following':is_following,


        }

        return render(request,'social/profile.html',context)



class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    #specify different attributes 

    model = UserProfile
    fields = ['name','bio','birth_date','location','picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk' : pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



class AddFollower(LoginRequiredMixin,UpdateView):
    def post(self,request,pk,*args,**kwargs):
        profile= UserProfile.objects.get(pk=pk)
        #to add followers
        #add method for ManyToMany Field
        profile.followers.add(request.user)

        #return to profile view

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect('profile',pk=profile.pk)


class RemoveFollower(LoginRequiredMixin,UpdateView):
    def post(self,request,pk,*args,**kwargs):
        profile= UserProfile.objects.get(pk=pk)
        #to remove followers
        #remove method for ManyToMany Field
        profile.followers.remove(request.user)

        #return to profile view
        return redirect('profile',pk=profile.pk)


class AddLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post= Post.objects.get(pk=pk)

        #checking if post has been disliked first before liking 
        is_dislike=False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)



        #like
        is_like=False

        #if user has already liked is_like variable is true
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        #if is_like is false -> add the like into the list
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

    #if post is already liked -> remove like (undo like)
        if is_like:
            post.likes.remove(request.user)  

        #getting the next value just passsed into the form
        next=request.POST.get('next','/') 
        #redirecting the http response
        return HttpResponseRedirect(next)   




class AddDislike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post= Post.objects.get(pk=pk)

        #checking if post has been liked first before disliking
        is_like=False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)



    #dislike
        is_dislike=False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)                
 
 
        next=request.POST.get('next','/') 
        return HttpResponseRedirect(next)   


class UserSearch(View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query) 
        )
        
        context= {
            'profile_list' : profile_list
        }
        return render(request,'social/search.html',context)


#view list of followers
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        #list of users following the user
        followers = profile.followers.all()

        context = {
            #access to profile and list of followers
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/followers_list.html', context)




class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)

class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')




class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'social/inbox.html', context)

class MakeThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'social/new_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create-thread')

class Thread(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'social/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )
        return redirect('thread', pk=pk)


class SharedPost(View):
    def post(self, request, pk, *args, **kwargs):
       original_post = Post.objects.get(pk=pk)
       form = ShareForm(request.POST)

       if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body=original_post.body,
                author=original_post.author,
                created_on=original_post.created_on,
                shared_user=request.user,
                shared_on=timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)

            new_post.save()

       return redirect('post-list')

class Explore(View) :
    #display all posts with the tag
    def get(self, request, *args, **kwargs):      
        explore_form=ExploreForm()
        query=self.request.GET.get('query')
        tag = Tag.objects.filter(name=query).first()

        #checking if the tag is in the tag field -> filtering by the tag
        if tag:
            posts= Post.objects.filter(tags__in=[tag])
        else:
            posts= Post.objects.all()

        context={
            'tag':tag,
            'posts': posts,
            'explore_form':explore_form
        }    

        return render(request,'social/explore.html',context)

    def post(self, request, *args, **kwargs):    
        explore_form=ExploreForm(request.POST)
        if explore_form.is_valid():
            query=explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()
            
            #shows nothing if no matching posts
            posts= None
            if tag:
                posts= Post.objects.filter(tags__in=[tag])

        #check if post exists
            if posts:
                context={
                    'tag':tag,
                    'posts':posts,
                    }    
            else:
                context={
                    'tag':tag,
                    }    
            return HttpResponseRedirect(f'/social/explore?query={query}')
        return HttpResponseRedirect('/social/explore')

            
