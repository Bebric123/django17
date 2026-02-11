from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит'
    )
    
    author_name = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора содержит'
    )
    
    date_after = DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    post_type = ChoiceFilter(
        field_name='post_type',
        label='Тип поста',
        choices=Post.POST_TYPES,
        empty_label='Все типы'
    )

    class Meta:
        model = Post
        fields = ['title', 'author_name', 'date_after', 'post_type']