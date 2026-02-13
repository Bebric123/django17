from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category, Subscription

@shared_task
def send_notification_about_new_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        categories = post.categories.all()
        
        subscribers_emails = []
        for category in categories:
            subscriptions = Subscription.objects.filter(category=category).select_related('user')
            for sub in subscriptions:
                if sub.user.email:
                    subscribers_emails.append(sub.user.email)
        
        subscribers_emails = list(set(subscribers_emails))
        
        if subscribers_emails:
            context = {
                'post': post,
                'categories': categories,
                'site_url': 'http://127.0.0.1:8000',
            }
            
            html_message = render_to_string('email/new_post_notification.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=f'Новая новость: {post.title}',
                message=plain_message,
                from_email='noreply@newsportal.com',
                recipient_list=subscribers_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            return f"Уведомления отправлены {len(subscribers_emails)} подписчикам"
        else:
            return "Нет подписчиков для уведомлений"
            
    except Exception as e:
        return f"Ошибка: {str(e)}"


@shared_task
def send_weekly_news():
    try:
        week_ago = timezone.now() - timedelta(days=7)
        recent_posts = Post.objects.filter(
            post_type='NW',
            created_at__gte=week_ago
        ).order_by('-created_at')

        users_with_email = User.objects.exclude(email='').exclude(email__isnull=True)
        
        total_emails_sent = 0
        
        for user in users_with_email:
            subscribed_categories = Category.objects.filter(
                subscriptions__user=user
            )
            
            user_news = recent_posts.filter(
                categories__in=subscribed_categories
            ).distinct()
            
            if user_news.exists():
                context = {
                    'user': user,
                    'news': user_news,
                    'site_url': 'http://127.0.0.1:8000',
                    'week_ago': week_ago.strftime('%d.%m.%Y'),
                }
                
                html_content = render_to_string('email/weekly_news_digest.html', context)
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(
                    subject=f'Еженедельный дайджест новостей',
                    body=text_content,
                    from_email='News Portal <noreply@newsportal.com>',
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                total_emails_sent += 1
        
        return f"Еженедельная рассылка отправлена {total_emails_sent} пользователям на почту"
        
    except Exception as e:
        return f"Ошибка при отправке еженедельной рассылки: {str(e)}"


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if user.email:
            context = {
                'user': user,
                'site_url': 'http://127.0.0.1:8000',
            }
            
            html_content = render_to_string('email/welcome_email.html', context)
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                subject=f'Добро пожаловать на News Portal!',
                body=text_content,
                from_email='News Portal <welcome@newsportal.com>',
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return f"Приветственное письмо отправлено пользователю {user.username}"
        else:
            return f"У пользователя {user.username} нет email"
            
    except User.DoesNotExist:
        return f"Пользователь с id {user_id} не найден"
    except Exception as e:
        return f"Ошибка при отправке приветственного письма: {str(e)}"