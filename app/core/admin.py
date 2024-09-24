from django.apps import apps
from django.contrib import admin

from core.models import Book, User

models = apps.get_models()


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "created_on",
    ]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "membership_id",
        "enrolled_on",
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.site_header = "Cowrywise Library Admin"
