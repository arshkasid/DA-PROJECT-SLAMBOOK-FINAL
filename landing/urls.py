from django.urls import path
from landing.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    #Index.as_view() will run to show index page
]
