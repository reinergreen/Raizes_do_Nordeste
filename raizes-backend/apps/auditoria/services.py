from .models import LogAuditoria


def registrar_log(usuario, acao, entidade, entidade_id='', detalhes=None):
    try:
        return LogAuditoria.objects.create(
            usuario=usuario if getattr(usuario, 'is_authenticated', False) else None,
            acao=acao,
            entidade=entidade,
            entidade_id=str(entidade_id or ''),
            detalhes=detalhes or {},
        )
    except Exception:
        # Log não deve derrubar o fluxo principal em projeto acadêmico.
        return None
