# MADR (Meu Acervo Digital de Romancistas)

API desenvolvida como trabalho de conclusão do curso FastAPI do Zero (https://fastapidozero.dunossauro.com/). A aplicação consiste em um sistema para gerenciamento de usuários, livros e romancistas. A aplicação utiliza FastAPI como framework principal e oferece funcionalidades de autenticação, cadastro de contas, gerenciamento de livros e autores.

## Estrutura do Projeto
```plaintext
.
├── alembic.ini                # Configuração de migrações para SQLite
├── alembic_postgresql.ini     # Configuração de migrações para PostgreSQL
├── database.db                # Banco de dados SQLite (ambiente de desenvolvimento)
├── Dockerfile                 # Arquivo para containerização da aplicação
├── entrypoint.sh              # Script de inicialização do container Docker
├── htmlcov/                   # Relatórios de cobertura de testes
├── madr/                      # Diretório principal da aplicação
│   ├── app.py                 # Arquivo principal da aplicação FastAPI
│   ├── database.py            # Configuração de conexão com o banco de dados
│   ├── models.py              # Definição dos modelos de dados (ORM)
│   ├── routers/               # Diretório contendo as rotas/endpoints da API
│   ├── schemas.py             # Esquemas de validação e serialização (Pydantic)
│   ├── security.py            # Implementação de autenticação e segurança
│   └── settings.py            # Configurações da aplicação
├── migrations/                # Diretório de migrações para SQLite
├── migrations_postgresql/     # Diretório de migrações para PostgreSQL
├── poetry.lock                # Arquivo de bloqueio de dependências do Poetry
├── pyproject.toml             # Configuração do projeto e dependências
├── README.md                  # Documentação da aplicação
└── tests/                     # Diretório de testes automatizados (pytest)
```

## Funcionalidades
- **Autenticação de Usuários**: Registro, login e gerenciamento de contas.
- **Gerenciamento de Livros**: CRUD de livros com informações detalhadas.
- **Gerenciamento de Romancistas**: CRUD de romancistas com biografias e obras.
- **Cobertura de Código**: Relatórios de cobertura para garantir qualidade nos testes.

## Requisitos
- Python 3.12+
- Poetry (para gerenciamento de dependências)
- Docker 

### Dependências de Desenvolvimento
- taskpy: ferramenta para criação de comandos (ex: executar aplicação, rodar testes, etc.)
- pytest: ferramenta para escrever e executar testes.
- ruff: ferramenta para análise estática e formatação de código. 

## Instalação
Clone o repositório:

```bash
git clone https://github.com/christyan-costa/madr.git
cd madr
```

Instale as dependências:
```bash
poetry install
```

Configure o banco de dados:

Para SQLite:

```bash
alembic upgrade head
```

Para PostgreSQL:

Configure o arquivo alembic_postgresql.ini com as credenciais do seu banco e execute:

```bash
alembic -c alembic_postgresql.ini upgrade head
```

## Executando a Aplicação

### Localmente
Para rodar a aplicação localmente, execute:

```bash
task run
```

Acesse a documentação interativa da API em http://localhost:8000/docs.

### Usando Docker
Construa o container:

```bash
docker build -t madr .
```

Execute o container:

```
docker run -p 8000:8000 madr
```

### Testes
Para executar os testes, use:
```
task test
```
