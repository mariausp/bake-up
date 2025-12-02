from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        ingredients = request.POST.get('ingredients')
        preparation = request.POST.get('preparation')
        image = request.FILES.get('image')

        # todos obrigatórios (você pode relaxar se quiser depois)
        if title and description and content and ingredients and preparation:
            post = Post.objects.create(
                title=title,
                description=description,
                content=content,
                ingredients=ingredients,
                preparation=preparation,
                image=image,
            )
            return redirect('blog:post_detail', pk=post.pk)

        # se faltar algo, você pode mandar uma mensagem de erro depois
    else:
        post = None

    return render(request, 'blog/post_form.html', {'post': post, 'page_title': 'Enviar uma nova receita'})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        # pega os valores editados do formulário
        post.title = request.POST.get('title', '').strip()
        post.description = request.POST.get('description', '').strip()
        post.content = request.POST.get('content', '').strip()
        post.ingredients = request.POST.get('ingredients', '').strip()
        post.preparation = request.POST.get('preparation', '').strip()

        image = request.FILES.get('image')
        if image:
            post.image = image

        # salva as mudanças
        post.save()

        # 👉 depois de salvar, VOLTA para a lista de receitas
        return redirect('blog:post_list')

    # GET: só mostra o formulário preenchido para edição
    return render(
        request,
        'blog/post_form.html',
        {'post': post, 'page_title': 'Editar receita'}
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
