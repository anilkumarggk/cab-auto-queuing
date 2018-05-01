from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        paginated_response = {
            'results_per_page': self.page_size,
            'total_results': self.page.paginator.count,
            'results': data,
            'current_page': self.page.number
        }
        paginated_response.update(self.get_html_context())
        return Response(paginated_response)
