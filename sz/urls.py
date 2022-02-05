from django.urls import path
from .views import ClientsView, TestView, TestView2, MatchView

urlpatterns = [
    path('clients/create/', ClientsView.as_view(), name='client'),
    path('clients/', TestView.as_view()),
    path('client/<int:pk>/', TestView2.as_view()),
    path('clients/<int:pk>/match/', MatchView.as_view(), name='match'),

]