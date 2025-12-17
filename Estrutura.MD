# Estrutura do Projeto EduPersona

Este arquivo descreve a organização das pastas e arquivos deste projeto, facilitando o entendimento da arquitetura e dos componentes disponíveis.

## Diretórios Principais

### `devops/`
Responsável pela configuração de ambiente e infraestrutura, focada principalmente no banco de dados.
- **`mysql/`**: Configurações para o container MySQL.
  - **`scripts-carga/`**: Contém scripts SQL executados na inicialização do container para popular o banco.
    - `01-dml.sql`: Scripts de manipulação de dados (inserts iniciais).
    - `02-ddl.sql`: Definição da estrutura do banco (tabelas, schemas).
  - **`scripts-consulta/`**: Scripts SQL auxiliares para consultas e verificações (ex: validação de dados de alunos e disciplinas).

### `src/`
Contém o código-fonte da aplicação Python.
- **`agents/`**: Scripts de definição e execução dos agentes inteligentes (ex: `edupersona-acompanhamento-desempenho.py`).


### `adm-educacional/`
Armazena recursos e dados educacionais auxiliares.
- **`objetos-de-aprendizagem/`**: Contém arquivos CSV (`oa.csv`) com metadados ou dados sobre objetos de aprendizagem utilizados pelo sistema.

## Arquivos na Raiz

- **`docker-compose.yml`**: Arquivo de orquestração do Docker. Define os serviços da aplicação, como o banco de dados e a configuração de redes/volumes necessária para rodar o ambiente.
- **`server.db`**: Arquivo de banco de dados criado pelo spade.
- **`requirements.txt`**: Lista as dependências Python necessárias para rodar o projeto.