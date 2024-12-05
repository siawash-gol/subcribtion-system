from django.urls import path, include
from rest_framework.routers import SimpleRouter
from config.apps.ClientHub.views.plan_views import PlansViewSet

router = SimpleRouter()
router.register('', PlansViewSet, basename='class')
urlpatterns = []
urlpatterns += router.urls
