from django.conf.urls import include, url
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'mls_listing', MLSListingViewSet)
router.register(r'mls_price', MLSPriceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
