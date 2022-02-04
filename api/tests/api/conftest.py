"""Global settings for Pytest"""

import pytest
from model_bakery import baker

from api.models import FavoriteCharacter, FavoriteQuote


@pytest.fixture()
def add_fav_character():
    """Fixture to help create bulk data for the Character model."""
    return baker.make(FavoriteCharacter)


@pytest.fixture()
def add_fav_quote():
    """Fixture to help create bulk data for the Character model."""
    return baker.make(FavoriteQuote)

@pytest.fixture()
def add_fav_quote():
    """Fixture to help create bulk data for the Character model."""
    return baker.make(FavoriteQuote)

