# Edupersona

## Sistema multiagente BDI para orientação personalizada de alunos via chat inteligente

Este projeto utiliza o framework [SPADE](https://spadeagents.eu/) para criar um sistema multiagente que oferece orientação personalizada para alunos através de um chat inteligente.

O sistema oferece uma avaliação do desempenho acadêmico de alunos em uma instituição de ensino fictícia.

O aluno interage com um chat informando sua matrícula e o que deseja, o sistema, por meio de agentes, realiza o diagnóstico do aluno e recomenda objetos de aprendizagem para o aprimoramento e evolução do aluno.

O aluno também pode interagir com o chat buscando objetos de aprendizagem para adquirir materias para aprofundamento em disciplinas de seu interesse.

## Estrutura de pastas
Veja mais detalhes na [Estrutura de Pastas](Estrutura.MD).

## Ferramentas

- Python
- Docker
- OpenAI

# Orientação da Instalação das Ferramentas

- Python - [Getting Started](https://www.python.org/about/gettingstarted/)
- Docker - [Instalação do Docker](https://docs.docker.com/manuals/)
- OpenAI - [Geração da API Key na OpenAI](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

## Instalação do Python 3.12.10
1. Acesse o link oficial: [Python 3.12.10](https://www.python.org/ftp/python/3.12.10/python-3.12.10-macos11.pkg)
2. Execute o instalador `.pkg` e siga as instruções na tela.

## Instalação do Docker via Homebrew
Abra o seu terminal e utilize o comando abaixo para instalar o Docker Desktop de forma rápida:

```bash
brew install docker
```

## Configuração da Aplicação
1.  **Crie um ambiente virtual (venv) com Python 3.12:**

    ```bash
    python3.12 -m venv edu_env
    ```

2.  **Ative o ambiente virtual:**

    ```bash
    source edu_env/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Adição da API Key na OpenAI na Aplicação**

    Acessar o arquivo `src/agent/edupersona-acompanhamento-desempenho.py`, procurar o trecho de código abaixo e adicionar sua chave no parâmetro `api_key`

    ```python
    provider = LLMProvider.create_openai(
        api_key="<OPENAI_API_KEY>",
        model="gpt-4o-mini",
        temperature=0.7
    )
    ```

## Execução

Vamos usar um terminal para cada um dos passos abaixo.

1.  **Inicie o servidor XMPP:**

    ```bash
    spade run
    ```

2.  **Inicie o banco de dados:**

    Em um novo terminal, execute:

    ```bash
    docker compose up
    ```

3.  **Execute os agentes:**

    Em um novo terminal, execute:

    ```bash
    python src/agent/edupersona-acompanhamento-desempenho.py
    ```

    A aplicação está executando, agora é só interagir com o chat.
