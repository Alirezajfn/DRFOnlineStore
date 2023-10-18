from rest_framework.pagination import PageNumberPagination


class DynamicProductsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        """
        If user is staff, return 1000 products per page, else return 100 products per page
        """
        if request.user.is_staff:
            self.max_page_size = 1000
        else:
            self.max_page_size = 100
        return super().paginate_queryset(queryset, request, view)
