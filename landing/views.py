from django.shortcuts import render

#importing generic views class
from django.views import View

#creating a class Index
class Index(View):

    #request is sent to the url
    def get(self, request, *args, **kwargs):
        return render(request, 'landing/Index.html')

