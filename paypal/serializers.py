import logging
from rest_framework import serializers
from store.models import Cart


logger = logging.getLogger(__name__)

class PaypalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields=('__all__')