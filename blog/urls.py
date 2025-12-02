from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/novo/', views.post_create, name='post_create'),
    path('posts/<int:pk>/editar/', views.post_update, name='post_update'),
    path('posts/<int:pk>/remover/', views.post_delete, name='post_delete'),

    # cadastro
    path('cadastro/', views.signup, name='signup'),
]
