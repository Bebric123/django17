from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .tasks import send_welcome_email

@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    try:
        group = Group.objects.get(name='common')
        user.groups.add(group)
        print(f"Пользователь {user.username} добавлен в группу common")
    except Group.DoesNotExist:
        print("Группа 'common' не найдена! Создайте её в админке.")

@receiver(post_save, sender=User)
def send_welcome_email_on_registration(sender, instance, created, **kwargs):
    if created and instance.email:
        send_welcome_email.delay(instance.id)