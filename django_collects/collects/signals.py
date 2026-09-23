from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Collect


@receiver(post_delete, sender=Collect)
def delete_cover_on_collect_delete(sender, instance, **kwargs):
    """Удаляет файл обложки с диска при удалении сбора (К4)."""
    if instance.cover:
        instance.cover.delete(save=False)