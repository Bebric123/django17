from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def add_user_to_common_group(request, user, **kwargs):
    """Добавляет пользователя в группу common при регистрации"""
    try:
        group = Group.objects.get(name='common')
        user.groups.add(group)
        print(f"Пользователь {user.username} добавлен в группу common")
    except Group.DoesNotExist:
        print("Группа 'common' не найдена! Создайте её в админке.")