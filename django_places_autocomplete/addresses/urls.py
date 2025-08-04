from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.address_form_view, name='address_form'),
    path('list/', views.address_list_view, name='address_list'),
    path('geocode/', views.geocode_view, name='geocode'),
]
