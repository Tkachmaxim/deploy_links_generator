from django.urls import path
from app import views


app_name = 'app'

urlpatterns = [
    path('', views.Start.as_view(), name='index'),
    path(r'<short_id>', views.ReturnShortLink.as_view(), name='return_short_link'),
]
