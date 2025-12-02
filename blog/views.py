from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # cria o objeto Post, mas ainda não salva
            post = form.save(commit=False)

           
            ingredientes_html = post.ingredients.replace('\n', '<br>')
            preparo_html      = post.preparation.replace('\n', '<br>')

            post.content = (
                "<h2>Ingredientes</h2>"
                f"<p>{ingredientes_html}</p>"
                "<h2>Modo de preparo</h2>"
                f"<p>{preparo_html}</p>"
            )

            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
        post = None  # para o preview de imagem não quebrar

    return render(
        request,
        'blog/post_form.html',
        {
            'form': form,
            'post': post,
            'page_title': 'Enviar uma nova receita'
        }
    )


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            ingredientes_html = post.ingredients.replace('\n', '<br>')
            preparo_html      = post.preparation.replace('\n', '<br>')

            post.content = (
                "<h2>Ingredientes</h2>"
                f"<p>{ingredientes_html}</p>"
                "<h2>Modo de preparo</h2>"
                f"<p>{preparo_html}</p>"
            )

            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/post_form.html',
        {
            'form': form,
            'post': post,
            'page_title': 'Editar receita'
        }
    )


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()              # cria o usuário
            return redirect('login') # depois vai para tela de login
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
