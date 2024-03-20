from rest_framework import serializers

from myapp.models import Goods, MyUser, Purchase, ReturnGoods
from django.utils import timezone


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ["name", "description", "price", "quantity"]


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["username", "wallet", "email"]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["product", "purchase_quantity"]

    def validate(self, data):
        super().validate(data)

        product = data['product']
        if product.quantity < data['purchase_quantity']:
            raise serializers.ValidationError('The quantity of goods purchased cannot be greater than the total quantity of goods.')

        if data['purchase_quantity'] <= 0:
            raise serializers.ValidationError('The number of purchased goods cannot be less than 1.')

        user = self.context['request'].user
        if user.wallet < product.price * data['purchase_quantity']:
            raise serializers.ValidationError('Insufficient funds')

        return data


class ReturnGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnGoods
        fields = ["purchase"]
        consent = serializers.BooleanField()

    def validate(self, data):
        super().validate(data)

        user = self.context['request'].user
        product = data['purchase']
        now = timezone.now()
        if now > (product.created_at + timezone.timedelta(minutes=3)):
            raise serializers.ValidationError('3 minutes to return have expired')

        if user.is_staff:
            return data

        if not product.client == user or user.is_admin:
            raise serializers.ValidationError('This user is not related to this purchase')

        return data