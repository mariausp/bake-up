# blog/models.py
from django.db import models
from django.conf import settings   # já estava aí


class Category(models.Model):
    name = models.CharField("Nome", max_length=100, unique=True)
    description = models.TextField("Descrição", blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    ingredients = models.TextField()
    preparation = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # categorias (parte 3)
    categories = models.ManyToManyField(
        Category,
        related_name='posts',
        blank=True
    )

    # curtidas
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )

    # favoritos
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_posts',
        blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def total_favorites(self):
        return self.favorites.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']   # mais recente primeiro

    def __str__(self):
        return f'Comentário de {self.author} em {self.post}'
