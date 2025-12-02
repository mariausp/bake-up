
from django import forms
from .models import Post, Comment   # <- IMPORTA Post E Comment AQUI EM CIMA


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'ingredients', 'preparation', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment          # <- agora Comment existe
        fields = ['text']        # ou o nome do campo de texto do seu Comment
