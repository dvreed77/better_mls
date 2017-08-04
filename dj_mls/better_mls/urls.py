from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^api/', include('base.urls'))
]

urlpatterns += staticfiles_urlpatterns()
