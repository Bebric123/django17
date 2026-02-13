from django.urls import path
from .views import (
    PostList, PostDetail, PostSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
    BecomeAuthorView, ProfileUpdateView, SubscriptionView,
    SubscribeView, UnsubscribeView, SubscribeWeeklyView
)

urlpatterns = [
    # Общие страницы
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),

    # ---------- НОВОСТИ ----------
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # ---------- СТАТЬИ ----------
    path('news/articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    path('become-author/', BecomeAuthorView.as_view(), name='become_author'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('subscribe/<int:category_id>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<int:category_id>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('subscribe-weekly/', SubscribeWeeklyView.as_view(), name='subscribe_weekly'),
]
