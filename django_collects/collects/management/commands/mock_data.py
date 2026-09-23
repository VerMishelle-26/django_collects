import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from collects.models import Collect, Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет БД моковыми данными"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=50)
        parser.add_argument("--collects", type=int, default=200)
        parser.add_argument("--payments", type=int, default=1000)

    def handle(self, *args, **options):
        users_count = options["users"]
        collects_count = options["collects"]
        payments_count = options["payments"]

        self.stdout.write("Создаю пользователей...")
        users = []
        for i in range(users_count):
            email = f"user{i}@example.com"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": f"user{i}"},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        self.stdout.write("Создаю сборы...")
        occasions = [c[0] for c in Collect.Occasion.choices]
        collects = []
        for i in range(collects_count):
            collect = Collect.objects.create(
                author=random.choice(users),
                title=f"Сбор #{i}",
                occasion=random.choice(occasions),
                description=f"Описание сбора #{i}",
                target_amount=random.choice([None, 10000, 50000, 100000]),
                ends_at=timezone.now() + timedelta(days=random.randint(1, 365)),
            )
            collects.append(collect)

        self.stdout.write("Создаю платежи...")
        for i in range(payments_count):
            collect = random.choice(collects)
            payment = Payment.objects.create(
                collect=collect,
                donor=random.choice(users),
                amount=random.randint(100, 5000),
                comment=f"Платёж #{i}",
            )
            collect.collected_amount += payment.amount
            collect.save(update_fields=["collected_amount"])

        self.stdout.write(self.style.SUCCESS(
            f"Готово! Создано: {users_count} польз., "
            f"{collects_count} сборов, {payments_count} платежей."
        ))