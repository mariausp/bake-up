# blog/urls.py
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    PostLikeToggleView,
    signup,
    logout_view,
    CategoryListView,
    CategoryPostListView,
    FavoriteToggleView,   # ⭐ novo
    FavoriteListView,     # ⭐ novo
)

app_name = 'blog'

urlpatterns = [
    # lista + home
    path('', PostListView.as_view(), name='post_list'),

    # detalhes do post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # CRUD de post (só logado)
    path('posts/novo/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/editar/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/remover/', PostDeleteView.as_view(), name='post_delete'),

    # comentários (parte 2)
    path('posts/<int:pk>/comentar/', CommentCreateView.as_view(), name='comment_create'),

    # like / deslike (toggle)
    path('posts/<int:pk>/like/', PostLikeToggleView.as_view(), name='post_like'),

    # favoritos
    path('posts/<int:pk>/favorite/', FavoriteToggleView.as_view(), name='post_favorite'),
    path('favoritos/', FavoriteListView.as_view(), name='favorites_list'),

    # categorias (parte 3)
    path('categorias/', CategoryListView.as_view(), name='category_list'),
    path('categorias/<int:pk>/', CategoryPostListView.as_view(), name='category_detail'),

    # auth simples
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
]
