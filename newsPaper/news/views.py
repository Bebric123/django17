from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import Group
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Author, User
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib import messages

LOGIN_URL = '/accounts/login/'

class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['post_count'] = self.get_queryset().count()
        return context
    
class PostSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# ---------- НОВОСТИ ----------
class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'  # NEWS
        return super().form_valid(form)

class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')
    
    def dispatch(self, request, *args, **kwargs):
        # Проверяем только группу, а не авторство
        if not (request.user.groups.filter(name='authors').exists() or request.user.is_superuser):
            messages.error(request, 'Только авторы могут редактировать новости!')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='NW')
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.groups.filter(name='authors').exists() or request.user.is_superuser):
            messages.error(request, 'Только авторы могут удалять новости!')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)

    
# ---------- СТАТЬИ ----------
class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR' 
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.groups.filter(name='authors').exists() or request.user.is_superuser):
            messages.error(request, 'Только авторы могут редактировать статьи!')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = '/accounts/login/'
    
    def get_queryset(self):
        return super().get_queryset().filter(post_type='AR')
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.groups.filter(name='authors').exists() or request.user.is_superuser):
            messages.error(request, 'Только авторы могут удалять статьи!')
            return redirect('post_list')
        return super().dispatch(request, *args, **kwargs)
    
class BecomeAuthorView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            authors_group, _ = Group.objects.get_or_create(name='authors')
            common_group = Group.objects.get(name='common')
            
            request.user.groups.remove(common_group)
            
            request.user.groups.add(authors_group)
            
            author, created = Author.objects.get_or_create(user=request.user)
            
            messages.success(request, 'Теперь вы автор!')
            
        except Group.DoesNotExist:
            messages.error(request, 'Группы не найдены. Создайте их в админке.')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
            
        return redirect(request.META.get('HTTP_REFERER', '/news/'))
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'account/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)