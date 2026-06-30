# Raízes do Nordeste - API Back-end

Projeto acadêmico da trilha Back-end para a rede **Raízes do Nordeste**. A API cobre o fluxo principal **Pedido -> Pagamento mock -> Atualização de status**, com autenticação JWT, perfis de acesso, estoque por unidade, cardápio por unidade, fidelidade, logs/auditoria e documentação Swagger.

## 1. Tecnologias

- Python 3.11+
- Django 5
- Django Rest Framework
- Simple JWT
- drf-spectacular / Swagger
- SQLite para teste local rápido
- PostgreSQL opcional via `DATABASE_URL`

## 2. Como rodar localmente

```bash
# 1) criar ambiente virtual
python -m venv .venv

# 2) ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3) instalar dependências
pip install -r requirements.txt

# 4) entrar na pasta
cd raizes-backend

# 5) criar arquivo de ambiente
copy .env.example .env
# no Linux/Mac: cp .env.example .env

# 6) criar banco e tabelas
python manage.py makemigrations
python manage.py migrate

# 7) popular dados de teste
python manage.py seed

# 8) iniciar API
python manage.py runserver
```

## 3. URLs principais

- API: `http://127.0.0.1:8000/api/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- Schema OpenAPI: `http://127.0.0.1:8000/api/schema/`
- Admin Django: `http://127.0.0.1:8000/admin/`

## 4. Usuários de teste

| Perfil | E-mail | Senha |
|---|---|---|
| ADMIN | admin@raizes.com | Admin@123 |
| GERENTE | gerente@raizes.com | Gerente@123 |
| ATENDENTE | atendente@raizes.com | Atendente@123 |
| COZINHA | cozinha@raizes.com | Cozinha@123 |
| CLIENTE | cliente@exemplo.com | Cliente@123 |

## 5. Fluxo principal para testar

1. Fazer login em `POST /api/auth/login/` com `cliente@exemplo.com`.
2. Copiar o campo `access` retornado.
3. Usar o header: `Authorization: Bearer <token>`.
4. Consultar cardápio: `GET /api/cardapio/?unidade_id=1`.
5. Criar pedido: `POST /api/pedidos/`.
6. Solicitar pagamento mock aprovado: `POST /api/pagamentos/mock/`.
7. Fazer login como cozinha ou gerente.
8. Atualizar status: `PATCH /api/pedidos/{id}/status/`.
9. Conferir auditoria: `GET /api/auditoria/logs/` com usuário gerente/admin.

Exemplo de criação de pedido:

```json
{
  "unidadeId": 1,
  "canalPedido": "TOTEM",
  "itens": [
    { "produtoId": 1, "quantidade": 2 }
  ],
  "formaPagamento": "MOCK"
}
```

## 6. Endpoints implementados

| Recurso | Endpoint | Descrição |
|---|---|---|
| Auth | `POST /api/auth/login/` | Login JWT |
| Auth | `POST /api/auth/refresh/` | Renovar token |
| Usuários | `POST /api/usuarios/` | Cadastro de cliente |
| Usuários | `GET /api/usuarios/me/` | Perfil autenticado |
| Unidades | `/api/unidades/` | CRUD de unidades |
| Produtos | `/api/produtos/` | CRUD de produtos |
| Cardápio | `/api/cardapio/` | Cardápio por unidade |
| Estoque | `GET /api/estoques/` | Consulta de estoque |
| Estoque | `POST /api/estoques/movimentar/` | Entrada, saída ou ajuste |
| Pedidos | `POST /api/pedidos/` | Criar pedido com canalPedido |
| Pedidos | `GET /api/pedidos/?canalPedido=TOTEM` | Filtro por canal |
| Pedidos | `PATCH /api/pedidos/{id}/status/` | Atualizar status |
| Pagamentos | `POST /api/pagamentos/mock/` | Simular pagamento |
| Fidelidade | `GET /api/fidelidade/saldo/` | Consultar saldo |
| Auditoria | `GET /api/auditoria/logs/` | Logs de ações sensíveis |

## 7. Padrão de erro

```json
{
  "error": "ESTOQUE_INSUFICIENTE",
  "message": "Não há quantidade suficiente para um ou mais itens.",
  "details": [
    { "field": "produtoId", "issue": "Saldo insuficiente" }
  ],
  "timestamp": "2026-02-05T12:00:00Z",
  "path": "/api/pedidos/"
}
```

## 8. Postman/Insomnia

A coleção está em:

`docs/postman/raizes_do_nordeste.postman_collection.json`

Ordem sugerida:

1. Auth/Login cliente
2. Cardápio/Listar por unidade
3. Pedidos/Criar pedido válido
4. Pagamentos/Mock aprovado
5. Auth/Login cozinha
6. Pedidos/Atualizar status para EM_PREPARO
7. Pedidos/Atualizar status para PRONTO
8. Auth/Login gerente
9. Auditoria/Listar logs
10. Testes negativos: sem token, canal inválido, estoque insuficiente, acesso sem permissão

## 9. Observações de segurança e LGPD

- Senhas são armazenadas com hash pelo mecanismo padrão do Django.
- Autenticação via JWT.
- Perfis/roles aplicados nos endpoints sensíveis.
- Dados pessoais mínimos: nome, e-mail, telefone opcional e consentimento de fidelidade.
- O programa de fidelidade só credita pontos se houver consentimento.
- Ações sensíveis geram logs em `LogAuditoria`.

## 10. Estrutura do projeto

```text

raizes-backend/
├── apps/
│   ├── auditoria/
│   ├── core/
│   ├── estoque/
│   ├── fidelidade/
│   ├── pagamentos/
│   ├── pedidos/
│   ├── produtos/
│   ├── unidades/
│   └── usuarios/
├── config/
├── docs/
├── manage.py
├── requirements.txt
└── .env.example
```


