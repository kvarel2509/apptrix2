from rest_framework import generics, status, views
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from django.core.mail import send_mass_mail
from .serializers import ClientSerializer, ReturnClientSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class ClientsView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(ReturnClientSerializer(serializer.data).data, status=status.HTTP_201_CREATED, headers=headers)


class TestView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ReturnClientSerializer


class TestView2(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ReturnClientSerializer


class MatchView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user_to_match = get_object_or_404(User, pk=pk)
        if user_to_match.pk == request.user.pk:
            return Response({'error': 'Нельзя добавить симпатию на самого себя'}, status=status.HTTP_409_CONFLICT)
        if not request.user.match.filter(pk=user_to_match.pk).exists():
            request.user.match.add(user_to_match)
            if user_to_match.match.filter(pk=request.user.pk).exists():
                send_mass_mail(((
                    'Взаимная симпатия',
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
