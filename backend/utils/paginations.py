from rest_framework.pagination import PageNumberPagination


class PageNumberWithPageSizeControllPagination(PageNumberPagination):
    page_size_query_param = 'limit'
