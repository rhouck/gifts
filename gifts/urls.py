from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gifts.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'gifts.views.splash', name='splash'),
    url(r'^our-gifts/$', 'gifts.views.gifts', name='gifts'),
    url(r'^privacy/$', 'gifts.views.privacy', name='privacy'),
    url(r'^terms-of-service/$', 'gifts.views.tos', name='tos'),
    url(r'^signup/$', 'gifts.views.signup', name='signup'),
    url(r'^confirmation/(?P<ref>[A-Za-z0-9]{8})$', 'gifts.views.confirmation', name='confirmation'),
    (r'^django-rq/', include('django_rq.urls')),

)
