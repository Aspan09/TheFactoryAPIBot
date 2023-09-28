from django.urls import include, path
from .views import RegisterUserView, AuthTokenObtainPairView, UserChatTokenListCreateView, SendMessageToTelegramView, \
    ArchiveMessageListView

urlpatterns = [
    # Регистрация пользователя
    path('register/', RegisterUserView.as_view(), name='register_user'),
    # {
    #     "email": "nurym@gmail.com",
    #     "password": "qwerty",
    #     "user_name": "nurym"
    # }
    #

    # Авторизация пользователя
    path('auth/', AuthTokenObtainPairView.as_view(), name='user_token'),
    # {
    # 	"email": "nurym@gmail.com",
    #   "password": "qwerty"
    # }

    # Генерация токена  POST запрос
    path('tokens/', UserChatTokenListCreateView.as_view(), name='user-chat-tokens'),
    #
    #   "chat_id" = "telegram_id" -- > пример chat_id = "8326382422"
    #

    # Отправка сообещении в телеграм Бот POST запрос
    path('send-message/', SendMessageToTelegramView.as_view(), name='send-message-to-telegram'),
    #
    #   "message" = "Привет мой друг"
    #

    # Вывод всех сообщении GET запрос
    path('all_message/', ArchiveMessageListView.as_view(), name='message_list'),
]
