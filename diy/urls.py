from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403, handler400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # Make sure base.urls exists and is correctly configured
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler404 = 'base.views.custom_404'
handler500 = 'base.views.custom_500'
handler403 = 'base.views.custom_403'
handler400 = 'base.views.custom_400'
