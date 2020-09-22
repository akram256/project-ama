import logging
from rest_framework import serializers
from store.models import Store


logger = logging.getLogger(__name__)

class PaypalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields=('id','product', 'price')

class ApprovePaymentSerializer(serializers.Serializer):
    payment_id = serializers.CharField()