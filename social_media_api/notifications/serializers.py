from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')
    target_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient_username', 'actor_username', 'verb',
                  'target_type', 'target_object_id', 'is_read', 'timestamp']

    def get_target_type(self, obj):
        return obj.target_content_type.model if obj.target_content_type else None
