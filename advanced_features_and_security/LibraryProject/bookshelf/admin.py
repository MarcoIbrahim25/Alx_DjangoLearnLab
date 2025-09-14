from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

class BookAdmin(admin.ModelAdmin):
    list_display  = ("title", "author", "publication_year")
    search_fields = ("title", "author")
    list_filter   = ("publication_year",)
    ordering      = ("title",)

admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

admin.site.register(CustomUser, CustomUserAdmin)
