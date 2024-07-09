from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    # path('', views.home,name="home"),
    path('ff/', views.users_view,name="users_view"),
    path('admin/', admin.site.urls),
    path('api/', include('usermanagement.urls')),
    path('api/', include('projectmanagement.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
