from django.urls import path
from .views import discrepancies_view

urlpatterns = [
    path("discrepancies/", discrepancies_view, name="discrepancies"),
]