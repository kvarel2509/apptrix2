from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import ClientSerializer, ReturnClientSerializer
from rest_framework.response import Response

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
