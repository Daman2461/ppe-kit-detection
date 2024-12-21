# crud_project/urls.py
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp import views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Serving the index.html as the home page
    path('files/', views.list_files, name='list_files'),
    path('webcam/', views.webcam_view, name='webcam_view'),
    path('webcam_feed/', views.webcam_prediction, name='webcam_prediction'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
