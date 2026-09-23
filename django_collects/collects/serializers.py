from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Collect, Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "avatar"]
        read_only_fields = ["id"]


class PaymentSerializer(serializers.ModelSerializer):
    donor = UserSerializer(read_only=True)
    collect = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "collect", "donor", "amount", "comment", "created_at"]
        read_only_fields = ["id", "donor", "collect", "created_at"]


class CollectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Collect
        fields = [
            "id", "author", "title", "occasion", "description",
            "target_amount", "collected_amount", "cover", "ends_at",
            "created_at", "updated_at", "payments",
        ]
        read_only_fields = ["id", "author", "collected_amount", "created_at", "updated_at"]