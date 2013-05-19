from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fantuan.views.home', name='home'),
    # url(r'^fantuan/', include('fantuan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/signup/', 'fantuan.user.signup'),
    url(r'^user/login/', 'fantuan.user.login'),
    url(r'^user/logout/', 'fantuan.user.logout'),
    url(r'^user/users/', 'fantuan.user.users'),
    url(r'^user/info/', 'fantuan.user.info'),
    url(r'^group/create/', 'fantuan.group.createGroup'),
    url(r'^group/join/', 'fantuan.group.joinGroup'),
    url(r'^group/opt/', 'fantuan.group.optGroup'),
    url(r'^$', 'fantuan.user.hello'),
)
