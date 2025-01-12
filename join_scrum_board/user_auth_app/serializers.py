from user_auth_app.models import PwResetTimestamp
from django.contrib.auth.models import User
from rest_framework import serializers

class PwResetTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = PwResetTimestamp
        fields = "__all__"