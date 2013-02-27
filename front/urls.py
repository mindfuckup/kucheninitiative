from django.conf.urls import patterns, include, url
from front import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^members/$', views.MemberView.as_view(), name='members'),
    url(r'^rules/$', views.RuleView.as_view(), name='rules'),
    url(r'^schedule/$', views.ScheduleView.as_view(), name='schedule'),
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),
)
