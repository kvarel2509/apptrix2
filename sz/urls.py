from django.urls import path
from .views import ClientsView

urlpatterns = [
    path('clients/create/', ClientsView.as_view(), name='client')
]