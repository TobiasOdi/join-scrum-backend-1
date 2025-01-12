from contacts_app.models import ContactItem
from django.contrib.auth.models import User
from rest_framework import serializers

class ContactItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactItem
        fields = "__all__"
