from django.urls import path

# app_name = 'v1'
from api.views import CharacterList, ApiRoot, CharacterQuoteDetail, FavoriteCharacterView, FavoriteList, FavoriteQuoteView

urlpatterns = [
    path('characters/', CharacterList.as_view(), name=CharacterList.name),
    path('characters/<str:pk>/quotes/', CharacterQuoteDetail.as_view(), name=CharacterQuoteDetail.name),
    path('characters/<str:pk>/favorites/', FavoriteCharacterView.as_view()),
    path('characters/<str:pk>/quotes/<str:id>/favorites/', FavoriteQuoteView.as_view()),
    path('favorites/', FavoriteList.as_view()),
    path('', ApiRoot.as_view(), name=ApiRoot.name),
]
