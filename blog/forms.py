from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # campos que o usuário vai preencher no formulário
        fields = ['title', 'description', 'ingredients', 'preparation', 'image']
