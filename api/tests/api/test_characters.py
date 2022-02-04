import pytest


@pytest.mark.django_db
def test_add_fav_character(client, add_fav_character):
    """Test to add a favorite characer."""
    headers = {'Authorization': "Token 3eaa49af34e6baaacb44ea6e187f41b4fbc3f585"}
    resp = client.post(
        "/api/characters/5cd99d4bde30eff6ebccfbbe/favorites/",
        {
            "character": "5cd99d4bde30eff6ebccfbbe",
        },
        headers=headers
    )
    assert resp.status_code == 201


@pytest.mark.django_db
def test_add_fav_character_invalid_json(client, add_fav_character):
    """Test if an empty json is sent"""
    headers = {'Authorization': "Token 3eaa49af34e6baaacb44ea6e187f41b4fbc3f585"}
    resp = client.post(
        "/api/characters/5cd99d4bde30eff6ebccfbbe/favorites/",
        {},
        content_type="application/json",
        headers=headers
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_add_fav_character_invalid_json_keys(client, add_fav_character):
    """Return 400 if the keys are not correct"""
    headers = {'Authorization': "Token 3eaa49af34e6baaacb44ea6e187f41b4fbc3f585"}
    resp = client.post(
        "/api/characters/5cd99d4bde30eff6ebccfbbe/favorites/",
        {
            "charter": "jaskdfkajsdfkjadshfjadsh",
        },
        content_type="application/json",
        headers=headers
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_add_fav_character_no_token(client, add_fav_character):
    """Return 400 if a token is not provided"""
    resp = client.post(
        "/api/characters/5cd99d4bde30eff6ebccfbbe/favorites/",
        {
            "charter": "jaskdfkajsdfkjadshfjadsh",
        },
        content_type="application/json",
    )
    assert resp.status_code == 401
