from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.cache import cache
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.db.models import F
from django.utils import timezone
from boardworld.permissions import IsOwnerOrReadOnly, AccessBlocked, IsOwnerOrAdmin
from boardworld.serializers import MyUserSerializer, GoodsSerializer, PurchaseSerializer, ReturnGoodsSerializer
from myapp.filters import IsOwnerFilterBackend
from myapp.models import MyUser, Goods, Purchase, ReturnGoods


class MyUserModelViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]

        if self.action == "destroy":
            return [IsAdminUser()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(wallet=10000)


class GoodsModelViewSet(ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "create":
            return [IsAdminUser()]

        if self.action == "update" or self.action == "partial_update":
            return [IsAdminUser()]

        if self.action == "destroy":
            return [AccessBlocked()]

        return super().get_permissions()


class PurchaseModelViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [IsOwnerFilterBackend]

    def get_permissions(self):
        if self.action == "list":
            return [IsOwnerOrAdmin()]

        if self.action == "destroy":
            return [IsAdminUser()]

        if self.action == "update" or self.action == "partial_update":
            return [AccessBlocked()]

        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        purchase_quantity = serializer.validated_data['purchase_quantity']
        user.wallet = F('wallet') - (purchase_quantity * product.price)
        user.save()

        product.quantity = F('quantity') - purchase_quantity
        product.save()

        serializer.save(client=user)

    def perform_destroy(self, instance):
        product = instance.product
        client = instance.client
        product.quantity = F('quantity') + instance.purchase_quantity
        product.save()
        client.wallet = F('wallet') + (instance.purchase_quantity * product.price)
        client.save()
        instance.delete()


class ReturnGoodsModelViewSet(ModelViewSet):
    queryset = ReturnGoods.objects.all()
    serializer_class = ReturnGoodsSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "create":
            return [IsAdminUser() or IsAuthenticated()]

        if self.action == "update" or self.action == "partial_update":
            return [AccessBlocked()]

        return super().get_permissions()


