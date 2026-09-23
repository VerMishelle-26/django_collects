from django.contrib import admin
from .models import User, Collect, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff")
    search_fields = ("username", "email")


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "occasion", "target_amount", "collected_amount", "ends_at")
    list_filter = ("occasion",)
    search_fields = ("title", "description")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "collect", "donor", "amount", "created_at")
    list_filter = ("collect",)