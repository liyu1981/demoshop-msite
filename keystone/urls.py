from django.conf.urls import include, url
from common import views as common_views


urlpatterns = [
    url(r'^$', common_views.home, name='home'),
    url(r'^demoshop/', include('demoshop.urls', namespace='demoshop')),
]
