from rest_framework.response import Response
from rest_framework.views import APIView



class StatusView(APIView):

    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'GitPack is running',
            'database': self.check_database_connection()
        })

    def check_database_connection(self):
        try:
            from django.db import connection
            connection.cursor().execute("SELECT 1")
            return 'ok'
        except Exception as e:
            return f'error: {str(e)}'