from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weekendplanner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', 'weekendplanner.views.search', name='search'),
    url(r'^$', 'weekendplanner.views.home', name='home'),
    url(r'^facebook_login/', 'weekendplanner.views.facebook_login', name='facebook_login'),
    url(r'^profile/', 'weekendplanner.views.profile', name='profile'),
    url(r'^logout/', 'weekendplanner.views.logout', name='logout'),
    url(r'^populate_database', 'weekendplanner.views.populate_database', name='populate_database'),
    url(r'^places', 'weekendplanner.views.places', name='places'),
    url(r'^event/', 'weekendplanner.views.event', name='event'),
)
