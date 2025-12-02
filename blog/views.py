from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views import View

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import PostForm, CommentForm


# ========== LISTA E DETALHE (públicos) ==========

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # comentários mais recentes primeiro
        context['comments'] = (
            post.comments.select_related('author')
            .order_by('-created_at')
        )

        # formulário vazio para comentar (se você quiser usar na mesma página)
        context['comment_form'] = CommentForm()
        return context


# ========== CRIAR / EDITAR / REMOVER POST (só logado) ==========

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Enviar uma nova receita'
        # usado no preview de imagem do template
        context.setdefault('post', None)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)

        # monta campo content em HTML bonitinho (ingredientes + preparo)
        ingredientes_html = post.ingredients.replace('\n', '<br>')
        preparo_html = post.preparation.replace('\n', '<br>')

        post.content = (
            "<h2>Ingredientes</h2>"
            f"<p>{ingredientes_html}</p>"
            "<h2>Modo de preparo</h2>"
            f"<p>{preparo_html}</p>"
        )

        post.save()
        self.object = post
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Editar receita'
        return context

    def form_valid(self, form):
        post = form.save(commit=False)

        ingredientes_html = post.ingredients.replace('\n', '<br>')
        preparo_html = post.preparation.replace('\n', '<br>')

        post.content = (
            "<h2>Ingredientes</h2>"
            f"<p>{ingredientes_html}</p>"
            "<h2>Modo de preparo</h2>"
            f"<p>{preparo_html}</p>"
        )

        post.save()
        self.object = post
        return redirect(self.get_success_url())

    def get_success_url(self):
        # depois de editar, volta para a lista de receitas
        return reverse('blog:post_list')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')


# ========== COMENTÁRIOS (parte 2) ==========

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        # pega o post da URL (/posts/<pk>/comentar/)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()

        return redirect('blog:post_detail', pk=post.pk)


# ========== LIKE / DESLIKE ==========

class PostLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        # volta para a página de onde veio (hidden next)
        next_url = request.POST.get('next')
        if not next_url:
            next_url = reverse('blog:post_detail', kwargs={'pk': pk})
        return redirect(next_url)


# ========== SIGNUP (view funcional) ==========

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
