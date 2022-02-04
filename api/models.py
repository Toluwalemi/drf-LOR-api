from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Timestamp(models.Model):
    """
    Timestamp mixin to inherit
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # prevent dj from creating a column for this table
    class Meta:
        abstract = True


class FavoriteCharacter(Timestamp):
    """
    Model to store favorite characters
    """
    user = models.ForeignKey('auth.User', related_name='characters', on_delete=models.CASCADE)
    character = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Favorite Characters"
        # different users can have similar favorite characters
        # but not same user. returns an error
        unique_together = ['user', 'character', ]

    def __str__(self):
        return f"{self.user.id} + {self.character}"


class FavoriteQuote(Timestamp):
    """
    Model to store favorite characters
    """
    user = models.ForeignKey('auth.User', related_name='quotes', on_delete=models.CASCADE)
    quote = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Favorite Quotes"
        unique_together = ['user', 'quote', ]

    def __str__(self):
        return f"{self.user.id} + {self.quote}"
