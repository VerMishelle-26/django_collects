from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Collect(models.Model):
    class Occasion(models.TextChoices):
        BIRTHDAY = "birthday", "День рождения"
        WEDDING = "wedding", "Свадьба"
        ANNIVERSARY = "anniversary", "Годовщина"
        GRADUATION = "graduation", "Выпускной"
        OTHER = "other", "Другое"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collects")
    title = models.CharField(max_length=200)
    occasion = models.CharField(max_length=20, choices=Occasion.choices, default=Occasion.OTHER)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(Decimal("0"))]
    )
    collected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.author.email})"

    @property
    def is_finished(self):
        from django.utils import timezone
        return self.ends_at < timezone.now()


class Payment(models.Model):
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE, related_name="payments")
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="payments")
    amount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    validators=[MinValueValidator(Decimal("0.01"))],
)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.donor} -> {self.collect.title}: {self.amount}"