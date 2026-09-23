from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .tasks import send_collect_created_email, send_payment_email


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.select_related("author").prefetch_related("payments__donor")
    serializer_class = CollectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["occasion", "author"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "ends_at", "collected_amount"]

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)
        send_collect_created_email.delay(collect.id)

    def list(self, request, *args, **kwargs):
        cache_key = f"collects_list_{request.GET.urlencode()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60)
        return response

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def donate(self, request, pk=None):
        collect = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(collect=collect, donor=request.user)
        collect.collected_amount += payment.amount
        collect.save(update_fields=["collected_amount"])
        cache.clear()
        send_payment_email.delay(payment.id)
        return Response(PaymentSerializer(payment).data, status=201)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("donor", "collect")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["collect", "donor"]