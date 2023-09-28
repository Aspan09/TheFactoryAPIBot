from django.contrib import admin
from .models import StandardUser, UserChatToken, ArchiveMessage


class StandardUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_superuser']        # Поля для отображения в списке администраторов
    list_filter = ['is_superuser']                  # Фильтры для списка администраторов
    search_fields = ['email', 'user_name']          # Поля, по которым можно выполнять поиск


admin.site.register(StandardUser, StandardUserAdmin)
admin.site.register(UserChatToken)
admin.site.register(ArchiveMessage)

