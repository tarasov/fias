from django.conf.urls import patterns, include, url

from main.views import AddressView

urlpatterns = patterns(
    '',
    url(r'^fias/', include('main.urls')),
    url(r'^api/addresses/', AddressView.as_view()),
)
