from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    """
    Helper class to set maximum limit to 50.
    The web service will never return more than 50 resources in a response.
    """
    max_limit = 50
