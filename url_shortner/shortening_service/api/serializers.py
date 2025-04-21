from rest_framework import serializers
from shortening_service.models import ShortenedURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model            = ShortenedURL
        fields           = '__all__'
        read_only_fields = ['id', 'shortCode', 'createdAt', 'updatedAt']

    def validate_url(self, value):

        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid URL.")

        if ShortenedURL.objects.filter(url=value).exists():
            raise serializers.ValidationError("This URL has already been shortened.")

        return value
