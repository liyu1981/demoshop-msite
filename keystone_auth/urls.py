from django.conf.urls import url
from django.contrib.auth import views as auth_views
from keystone_auth import views


urlpatterns = [
    url(r'^login/$', auth_views.login,
        {'template_name': 'keystone_auth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'keystone_auth/logout.html'}, name='logout'),
    url(r'^register/$', views.register, name="register"),
    url(r'^fbuser/$', views.fbuser, name='fbuser'),
    url(r'^fbuser/delete/(?P<pk>\d+)/$', views.FBUserDeleteView.as_view(),
        name="delete_fbuser"),
    url(r'^fboauth/$', views.fboauth, name='fboauth'),
    url(r'^fbcallback/$', views.fbcallback, name='fbcallback'),
]
