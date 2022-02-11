
from django.urls import path
from .views import ClientsView, UserListView, MatchView

urlpatterns = [
    path('clients/create/', ClientsView.as_view(), name='client'),
    path('list/', UserListView.as_view()),
    path('clients/<int:pk>/match/', MatchView.as_view(), name='match'),

]

