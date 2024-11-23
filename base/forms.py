from django import forms
from django.forms import ModelForm
from . import models
from django.contrib.auth.forms import AuthenticationForm

class TopicForm(ModelForm):
  class Meta:
    model = models.Topic
    fields = '__all__'
    exclude = ['course']  


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['caption']

class MediaForm(forms.ModelForm):
    class Meta:
        model = models.Media
        fields = ['file']

# Update the formset to exclude the delete checkbox
MediaFormSet = forms.inlineformset_factory(models.Post, models.Media, form=MediaForm, extra=1, can_delete=False)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
