from django.conf.urls import include, url
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'mls_complete', MLSCompleteViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
