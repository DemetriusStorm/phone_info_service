from django.urls import path
from .views import PhoneCheckView, PhoneHistoryView

urlpatterns = [
    path('', PhoneCheckView.as_view(), name='check_phone'),
    path('history/', PhoneHistoryView.as_view(), name='history'),
]