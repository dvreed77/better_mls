from rest_framework import serializers
from .models import *




class MLSPriceSerializer(serializers.ModelSerializer):
    # mls = serializers.HyperlinkedRelatedField(
    #     many=False,
    #     read_only=True,
    #     view_name='mls_listing-detail',
    #     lookup_field='mls'
    # )
    class Meta:
        model = MLSPrice
        fields = ('price',)

class MLSPriceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLSPrice
        fields = ('price', 'status', 'datetime',)

class MLSListingSerializer(serializers.ModelSerializer):
    # prices = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mls_price-detail',
    #     lookup_field='mls'
    # )
    # prices = MLSPriceSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = MLSListing
        fields = '__all__'
