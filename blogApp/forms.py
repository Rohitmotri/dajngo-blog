from django import forms
from blogApp.models import *


class PostForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Post
        fields = ("title","title_tag","img","body","category","featured")


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("message",)
