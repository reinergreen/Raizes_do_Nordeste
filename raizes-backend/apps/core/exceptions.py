from django.utils import timezone
from rest_framework.views import exception_handler


def exception_handler_padrao(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    path = request.path if request else ''

    if response is None:
        return response

    detail = response.data
    details = []
    message = 'Erro na requisição.'

    if isinstance(detail, dict):
        if 'detail' in detail:
            message = str(detail['detail'])
        else:
            for field, issues in detail.items():
                if not isinstance(issues, list):
                    issues = [issues]
                for issue in issues:
                    details.append({'field': field, 'issue': str(issue)})
            if details:
                message = 'Existem campos inválidos na requisição.'
    elif isinstance(detail, list):
        details = [{'field': 'non_field_errors', 'issue': str(item)} for item in detail]

    error_name = {
        400: 'REQUISICAO_INVALIDA',
        401: 'NAO_AUTENTICADO',
        403: 'SEM_PERMISSAO',
        404: 'NAO_ENCONTRADO',
        409: 'CONFLITO_REGRA_NEGOCIO',
        422: 'VALIDACAO_INVALIDA',
    }.get(response.status_code, 'ERRO')

    response.data = {
        'error': error_name,
        'message': message,
        'details': details,
        'timestamp': timezone.now().isoformat(),
        'path': path,
    }
    return response
