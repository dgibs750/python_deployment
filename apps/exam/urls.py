from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^register_form/$', views.register_form),
    url(r'^add_user/$', views.add_user),
    url(r'^quotes/$', views.dashboard),
    url(r'^user/(?P<num>\d+)/$', views.userQuotes),
    url(r'^myaccount/(?P<num>\d+)/$', views.myAccount),
    url(r'^addQuote/$', views.add_quote),
    url(r'^update/$', views.update),
    url(r'^logout/$', views.logout),
    url(r'^delete/(?P<num>\d+)/$', views.delete),
    url(r'^like/(?P<num>\d+)/$', views.like)
]