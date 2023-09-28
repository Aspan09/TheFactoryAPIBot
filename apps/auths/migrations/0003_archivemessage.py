# Generated by Django 4.2.5 on 2023-09-27 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_alter_userchattoken_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.TextField()),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение пользователя',
                'verbose_name_plural': 'Сообщении пользователей',
            },
        ),
    ]
