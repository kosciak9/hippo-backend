from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from hippo.users.views import (AvailabilityViewSet, PositionViewSet,
                               TeamViewSet, UserViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'availablity', AvailabilityViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router.urls)),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'),
                                        permanent=False)),

]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls',
                                  namespace='rest_framework'))
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
