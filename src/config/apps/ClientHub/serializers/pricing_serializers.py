from rest_framework import serializers
from config.apps.ClientHub.models import Plan


class AllPlansSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Plan
        fields = [
            'id',
            'slug',
            'plan',
            'category',
            'price',
            'get_features',
            'get_duration',
        ]


class DetailPlanSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Plan
        fields = [
            'id',
            'plan',
            'category',
            'slug',
            'price',
            'get_features',
            'get_duration',
        ]
