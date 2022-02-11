from rest_framework import generics, status, views
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mass_mail
from .serializers import ClientSerializer, ReturnClientsListSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models.functions.math import Sin, Cos, ACos, Abs, Radians
from django.db.models import F
from decimal import Decimal

User = get_user_model()


class ClientsView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientSerializer


class UserFilter(filters.FilterSet):
    distance = filters.NumberFilter(field_name='distance', lookup_expr='lte', label='Расстояние')

    class Meta:
        model = User
        fields = ['gender', 'first_name', 'last_name', 'distance']


class UserListView(generics.ListAPIView):
    serializer_class = ReturnClientsListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        x1 = Radians(self.request.user.latitude)
        x2 = Radians(self.request.user.longitude)
        d = Decimal(6371.009)
        return User.objects.annotate(
            distance=d * ACos(
                Sin(x1) * Sin(Radians(F('latitude'))) + Cos(x1) * Cos(Radians(F('latitude'))) * Cos(
                    Abs(x2 - Radians(F('longitude')))))
        )


class MatchView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        user_to_match = get_object_or_404(User, pk=pk)
        if user_to_match.pk == request.user.pk:
            return Response({'error': 'Нельзя добавить симпатию на самого себя'}, status=status.HTTP_409_CONFLICT)
        if not request.user.match.filter(pk=user_to_match.pk).exists():
            request.user.match.add(user_to_match)
            if user_to_match.match.filter(pk=request.user.pk).exists():
                send_mass_mail((('Взаимная симпатия',
                                 f'Отмечена взаимная симпатия с {request.user.first_name + request.user.last_name}, '
                                 f'его email {request.user.email}',
                                 'kvarel_test@mail.ru',
                                 [user_to_match.email]
                                 ),
                                ('Взаимная симпатия',
                                 f'Отмечена взаимная симпатия с {user_to_match.first_name + user_to_match.last_name}, '
                                 f'его email {user_to_match.email}',
                                 'kvarel_test@mail.ru',
                                 [request.user.email])
                                ))
                return Response({'status': f'Взаимная симпатия, емаил - {user_to_match.email}'},
                                status=status.HTTP_207_MULTI_STATUS)
            else:
                return Response({'status': 'Симпатия добавлена'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Симпатия была проявлена ранее'}, status=status.HTTP_304_NOT_MODIFIED)
