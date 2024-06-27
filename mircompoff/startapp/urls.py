from django.urls import path
from .views import IndexPage


app_name = "startapp"

urlpatterns = [
    path('', IndexPage.as_view(), name="indexpage"),
]