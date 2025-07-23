🧩 Requisições no Swagger com Pydantic (FastAPI + SQLite)
Este é um projeto simples de API REST feita com FastAPI, utilizando Pydantic para validação de dados e SQLite como banco de dados. Ele permite criar, listar, atualizar e deletar usuários por meio de requisições visíveis no Swagger (documentação automática).

🚀 Tecnologias usadas
Python 3.10+

FastAPI

SQLite3

Pydantic

Uvicorn (para rodar o servidor)

▶️ Como rodar
Execute o comando abaixo para iniciar o servidor FastAPI:

📘 Documentação automática
Swagger UI:
👉 http://127.0.0.1:8000/docs

Redoc:
👉 http://127.0.0.1:8000/redoc

📚 Endpoints disponíveis
Método	Rota	Descrição
GET	/	Página inicial
POST	/usuario/	Cria um novo usuário
GET	/usuario/	Lista todos os usuários
GET	/usuario/{id}	Busca um usuário por ID
PUT	/usuario/{id}	Atualiza um usuário por ID
DELETE	/usuarios/{id}	Deleta um usuário por ID

📁 Estrutura básica
bash
Copiar
Editar
.
├── banco.db            # Banco de dados SQLite
├── main.py             # Arquivo principal com as rotas
└── README.md           # Documentação do projeto
✅ Exemplo de JSON para criação de usuário
json
Copiar
Editar
{
  "nome": "João Pedro",
  "email": "joao@example.com"
}
📌 Observações
O banco de dados SQLite é criado automaticamente na primeira execução.

As requisições podem ser testadas diretamente na interface Swagger.
