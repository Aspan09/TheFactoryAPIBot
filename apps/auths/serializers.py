from rest_framework import serializers
from .models import StandardUser, UserChatToken, ArchiveMessage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardUser
        fields = ['id', 'email', 'password', 'user_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = StandardUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Включаем ID пользователя в токен
        token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Включаем ID пользователя в данные ответа
        data['id'] = self.user.id
        return data


class UserChatTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChatToken
        fields = ('user', 'chat_id', 'token',)


class ArchiveMessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArchiveMessage
        fields = ('sender', 'message_content', 'sent_date')
