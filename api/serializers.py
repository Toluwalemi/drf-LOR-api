from rest_framework import serializers

from api.models import FavoriteQuote, FavoriteCharacter


class FavoriteCharacterSerializer(serializers.ModelSerializer):
    # Display the user's username (read-only)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FavoriteCharacter
        fields = ('character', 'user',)
        read_only_fields = ('created', 'updated')


class FavoriteQuoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FavoriteQuote
        fields = ('quote', 'user',)
        read_only_fields = ('created', 'updated',)
