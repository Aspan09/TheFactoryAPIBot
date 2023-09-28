import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, user_name=None):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(email=self.normalize_email(email))
        if user_name:
            user.id_telegram = user_name

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, user_name=None):
        user = self.create_user(email, password, user_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class StandardUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    user_name = models.CharField(max_length=100, unique=True, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserChatToken(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Генерируем токен по умолчанию
    chat_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.user_name


class ArchiveMessage(models.Model):
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user_name}"

    class Meta:
        verbose_name = "Сообщение пользователя"
        verbose_name_plural = "Сообщении пользователей"


