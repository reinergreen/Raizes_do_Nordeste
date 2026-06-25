from django.utils import timezone
from rest_framework.response import Response


def erro_regra_negocio(error, message, status_code=409, details=None, path=''):
    return Response({
        'error': error,
        'message': message,
        'details': details or [],
        'timestamp': timezone.now().isoformat(),
        'path': path,
    }, status=status_code)
