from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Оставляем один путь, который загружает и форму, и отчёты
    path('', views.dashboard_view, name='dashboard'),
    path('delete/<str:model_name>/<int:item_id>/', views.delete_item, name='delete_item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)