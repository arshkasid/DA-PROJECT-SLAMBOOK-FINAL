#importing path and view

from django.urls import path
from .views import PostListView, PostDetailView, PostEditView, PostDeleteView ,CommentDeleteView,ProfileView,ProfileEditView,AddFollower,RemoveFollower,AddDislike,AddLike,UserSearch,ListFollowers,ListThreads,MakeThread,CreateMessage,Thread,  PostNotification, FollowNotification, RemoveNotification, ThreadNotification, SharedPost,Explore


#creating url patterns for views we just created
urlpatterns=[
    #creating a new path and put it at the root
    path('',PostListView.as_view(), name='post-list'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #what int:pk does is takes int in the variable p and each post is stored in a number

    #url for edit
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),

    #url for post delete
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),

    #url for comment delete
    #<int:post_pk> -> post ID ; 
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),

    #url -> addlike
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),

    #url ->dislike
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),

    #url for profile template i.e. profile.html
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),

    #url for profile edit
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),

    #url for adding followers
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),

    #url for removing followers
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),

    #url for search
    path('search/', UserSearch.as_view(), name='profile-search'),

    #url for names of followers
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),

    # url for post notifications
    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),

    # url for follow notification
    path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follow-notification'),

    # url for thread notifucation
    path('notification/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread-notification'),

    # url for removing notification
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),

    # url to see all threads
    path('inbox/', ListThreads.as_view(), name='inbox'),

    #url for explore
    path('explore/', Explore.as_view(), name='explore'),

    # url to create a new thread
    path('inbox/create-thread/', MakeThread.as_view(), name='create-thread'),

    # url to view a thread
    path('inbox/<int:pk>/', Thread.as_view(), name='thread'),

    # url ro create new messages
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),

    # url for shared posts
    path('post/<int:pk>/share', SharedPost.as_view(), name='share-post'),

]
