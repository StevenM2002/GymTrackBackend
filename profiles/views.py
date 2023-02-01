from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class SignUpAPI(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(validated_data=serializer.validated_data)
            token = Token.objects.get(user=user).key
            return Response({"token": token})
        return Response(serializer.errors, status=400)


class Signer(APIView):
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user:
            return Response(False)
        else:
            return Response(True)