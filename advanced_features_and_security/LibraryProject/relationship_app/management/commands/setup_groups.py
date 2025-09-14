from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ct = ContentType.objects.get_for_model(Book)
        codenames = ["can_view", "can_create", "can_edit", "can_delete"]
        perms = {p.codename: p for p in Permission.objects.filter(content_type=ct, codename__in=codenames)}

        viewers, _ = Group.objects.get_or_create(name="Viewers")
        viewers.permissions.set([perms["can_view"]])

        editors, _ = Group.objects.get_or_create(name="Editors")
        editors.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"]])

        admins, _ = Group.objects.get_or_create(name="Admins")
        admins.permissions.set([perms["can_view"], perms["can_create"], perms["can_edit"], perms["can_delete"]])
