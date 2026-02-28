from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect /admin to /myadmin
    path('admin/', RedirectView.as_view(url='/myadmin/', permanent=False)),
    path('myadmin/', include('shop.urls_admin')),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
