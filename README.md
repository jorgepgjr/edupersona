# Edupersona

## Sistema multiagente BDI para orientação personalizada de alunos via chat inteligente

Este projeto utiliza o framework [SPADE](https://spadeagents.eu/) para criar um sistema multiagente que oferece orientação personalizada para alunos através de um chat inteligente.

O sistema oferece uma avaliação do desempenho acadêmico de alunos em uma instituição de ensino fictícia.

O aluno interage com um chat informando sua matrícula e o que deseja, o sistema, por meio de agentes, realiza o diagnóstico do aluno e recomenda objetos de aprendizagem para o aprimoramento e evolução do aluno.

O aluno também pode interagir com o chat buscando objetos de aprendizagem para adquirir materias para aprofundamento em disciplinas de seu interesse.

## Ferramentas

- Python
- Docker
- OpenAI

## Orientação da Instalação das Ferramentas

- Python - [Getting Started](https://www.python.org/about/gettingstarted/)
- Docker - [Instalação do Docker](https://docs.docker.com/manuals/)
- OpenAI - [Geração da API Key na OpenAI](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

## Configuração da Aplicação

Siga os passos abaixo para configurar e executar o projeto:

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

    **Adição da API Key na OpenAI na Aplicação**

    Acessar o arquivo `src/agent/edupersona-acompanhamento-desempenho.py`, procurar o trecho de código abaixo e adicionar sua chave no parâmetro `api_key`

    ```python
    provider = LLMProvider.create_openai(
        api_key="<OPENAI_API_KEY>",
        model="gpt-4o-mini",
        temperature=0.7
    )
    ```

## Execução

4.  **Inicie o servidor XMPP:**

    ```bash
    spade run
    ```

5.  **Inicie o banco de dados:**

    Em um novo terminal, execute:

    ```bash
    docker compose up
    ```

6.  **Execute os agentes:**

    Em um novo terminal, execute:

    ```bash
    python src/agent/edupersona-acompanhamento-desempenho.py
    ```

    A aplicação está executando, agora é só interagir com o chat.
