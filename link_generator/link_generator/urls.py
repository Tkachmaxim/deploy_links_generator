from django.contrib import admin
from django.urls import path
from app.views import Start, ReturnShortLink


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Start.as_view(), name='index'),
    path(r'<short_id>', ReturnShortLink.as_view(), name='return_short_link'),
]
