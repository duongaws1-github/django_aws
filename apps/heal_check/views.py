from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class HealCheckViewSet(ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response(data={'OK!'}, status=status.HTTP_200_OK)
