import os
from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer, AuthTokenObtainPairSerializer, UserChatTokenSerializer, \
    ArchiveMessageSerializers
from .models import StandardUser, UserChatToken, ArchiveMessage
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import requests
from rest_framework.views import APIView


class RegisterUserView(generics.CreateAPIView):
    queryset = StandardUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer


class UserChatTokenListCreateView(generics.ListCreateAPIView):
    queryset = UserChatToken.objects.all()
    serializer_class = UserChatTokenSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SendMessageToTelegramView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        token = UserChatToken.objects.filter(user=user).first()

        if not token:
            return Response({'error': 'У пользователя нет действительного токена'}, status=400)

        chat_id = token.chat_id
        message_content = f'{user.user_name}, я получил от тебя сообщение:\n{request.data.get("message")}'

        telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        telegram_api_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'

        data = {
            'chat_id': chat_id,
            'text': message_content,
        }

        sender = user
        if sender:
            ArchiveMessage.objects.create(
                sender=sender,
                message_content=message_content
            )

        response = requests.post(telegram_api_url, data=data)

        if response.status_code == 200:
            return Response({'message': 'Сообщение успешно отправлено в Telegram'})
        else:
            return Response({'error': 'Не удалось отправить сообщение в Telegram'}, status=500)


class ArchiveMessageListView(generics.ListCreateAPIView):
    queryset = ArchiveMessage.objects.all()
    serializer_class = ArchiveMessageSerializers
    permission_classes = (IsAuthenticated,)

