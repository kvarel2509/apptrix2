from django.urls import path
from .views import ClientsView, TestView, TestView2

urlpatterns = [
    path('clients/create/', ClientsView.as_view(), name='client'),
    path('clients/', TestView.as_view()),
    path('client/<int:pk>', TestView2.as_view())
]