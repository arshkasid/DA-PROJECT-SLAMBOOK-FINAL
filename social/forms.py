#creatig adjango form -> creates a model html form ->creates it based on a model object

#importing forms and models
from django import forms
from .models import Post, Comment , MessageModel

class PostForm(forms.ModelForm): #inheriting from forms.ModelForm

    #set a variable equal to each field
    body = forms.CharField(
        label='', #keeping nothing written on the top of the post box
        widget=forms.Textarea(attrs={
            'rows' : '3', #shows 3 rows at a time
            'placeholder' : 'Type Something ...' #written inside the box 
        }))
    #optional fill
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )

    class Meta:
        #putting the data we want from form

        model = Post #so form knows we want the Post model
        
        #image is an optional field
        fields = ['body']


class CommentForm(forms.ModelForm): #inheriting from forms.ModelForm

    #set a variable equal to each field
    comment = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={
            'rows' : '3', #shows 3 rows at a time
            'placeholder' : 'Type Something ...' #written inside the box 
        }))


    class Meta:
        #putting the data we want from form

        model = Comment #so form knows we want the Post model
        fields=['comment']






class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']


class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))


class ExploreForm(forms.Form):
    #search for tags that match the query
    query=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder':'Explore tags'
        }))
    