from django.contrib import admin
from .models import Post, Profile, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "content")
    list_filter = ("published_date",)

admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
