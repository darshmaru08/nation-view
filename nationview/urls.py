from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth.views import LogoutView # Add this import
from core.views import custom_logout 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('citizen/', include('citizen.urls')),
    path('government/', include('government.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
