from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from config.apps.ClientHub.serializers.pricing_serializers import AllPlansSerializer, DetailPlanSerializer
from rest_framework.exceptions import NotAcceptable
from config.apps.ClientHub.models import Plan
from rest_framework import viewsets, status, exceptions
from django.conf import settings
import paypalrestsdk


class PlansViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Plan.objects.filter(somefilter)
    lookup_field = 'slug'

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return AllPlansSerializer
            case 'retrieve':
                return DetailPlanSerializer
            case _:
                raise NotAcceptable()
