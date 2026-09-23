from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Collect, Payment


@shared_task
def send_collect_created_email(collect_id):
    try:
        collect = Collect.objects.select_related("author").get(id=collect_id)
    except Collect.DoesNotExist:
        return
    send_mail(
        subject=f"Сбор '{collect.title}' создан",
        message=f"Ваш сбор '{collect.title}' успешно создан.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[collect.author.email],
        fail_silently=True,
    )


@shared_task
def send_payment_email(payment_id):
    try:
        payment = Payment.objects.select_related("donor", "collect").get(id=payment_id)
    except Payment.DoesNotExist:
        return
    send_mail(
        subject="Платёж получен",
        message=f"Вы внесли {payment.amount} в сбор '{payment.collect.title}'.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[payment.donor.email],
        fail_silently=True,
    )