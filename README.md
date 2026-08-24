# EDUPersona

## Sistema multiagente BDI para orientação personalizada de alunos via chat inteligente

Este projeto utiliza o framework [SPADE](https://spadeagents.eu/) para criar um sistema multiagente que oferece orientação personalizada para alunos através de um chat inteligente.

O sistema oferece uma avaliação do desempenho acadêmico de alunos em uma instituição de ensino fictícia.

O aluno interage com um chat informando sua matrícula e o que deseja, o sistema, por meio de agentes, realiza o diagnóstico do aluno e recomenda objetos de aprendizagem para o aprimoramento e evolução do aluno.

O aluno também pode interagir com o chat buscando objetos de aprendizagem para adquirir materiais para aprofundamento em disciplinas de seu interesse.

## Estrutura de Pastas

Veja mais detalhes na [Estrutura de Pastas](Estrutura.MD).

## Ferramentas

- Python
- Docker
- OpenAI

---

# Instalação das Ferramentas e Pré-requisitos

### macOS (Homebrew)

- **Python**: [Getting Started](https://www.python.org/about/gettingstarted/) ou via instalador oficial macOS: [Python 3.12.10 (.pkg)](https://www.python.org/ftp/python/3.12.10/python-3.12.10-macos11.pkg)
- **Docker**:
  ```bash
  brew install docker
  ```

### Windows (Ubuntu via WSL / Linux Ubuntu 24.04)

Caso esteja utilizando o Windows com **WSL (Ubuntu 24.04)** ou ambiente Linux Debian/Ubuntu, instale o Python, o gerenciador de pacotes e o módulo de ambientes virtuais:

```bash
# Atualize os repositórios
sudo apt update

# Instale o Python 3, pip e o módulo de venv
sudo apt install python3 python3-pip python3-venv -y

# Instale o Docker e o plugin do Docker Compose
sudo apt install docker.io docker-compose-v2 -y

# (Opcional) Adicione seu usuário ao grupo docker para executar sem sudo:
sudo usermod -aG docker $USER
```

> **Nota para Windows**: Se preferir, você também pode instalar o [Docker Desktop para Windows](https://docs.docker.com/desktop/setup/install/windows-install/) integrado ao WSL2.

- **OpenAI**: [Como gerar uma API Key na OpenAI](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

---

## Configuração da Aplicação

1. **Crie um ambiente virtual (venv):**

   ```bash
   python3 -m venv edu_env
   ```

2. **Ative o ambiente virtual:**
   - No Linux / macOS / WSL:
     ```bash
     source edu_env/bin/activate
     ```
   - No Windows (PowerShell):
     ```powershell
     .\edu_env\Scripts\Activate.ps1
     ```

3. **Instale as dependências do projeto:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração da Chave da OpenAI:**

   Acesse o arquivo `src/agents/edupersona-acompanhamento-desempenho.py`, localize o trecho abaixo e adicione sua chave:

   ```python
   provider = LLMProvider.create_openai(
       api_key="<SUA_OPENAI_API_KEY>",
       model="gpt-4o-mini",
       temperature=0.7
   )
   ```

---

## Execução

Recomenda-se utilizar um terminal dedicado para cada um dos passos a seguir:

1. **Inicie o servidor XMPP:**

   _(Certifique-se de estar com o ambiente virtual ativado)_

   ```bash
   spade run
   ```

2. **Inicie o banco de dados via Docker:**

   > **Importante:** Certifique-se de que o Docker está em execução e que o plugin `docker-compose-v2` está instalado (`sudo apt install docker-compose-v2` no Ubuntu/WSL).

   Em um novo terminal, suba o container do banco:

   ```bash
   docker compose up
   ```

   _(Caso utilize a versão legada do Compose, o comando pode ser `docker-compose up`)_.

   > **Dica de Solução de Problemas:** Se o banco não inicializar ou apresentar erro de permissão no WSL/Linux:
   >
   > - Verifique se o daemon do Docker está rodando com `sudo service docker status` (ou inicie com `sudo service docker start`).
   > - Se necessário, execute com permissão de superusuário: `sudo docker compose up`.

3. **Execute os agentes:**

   Em um novo terminal (com o `edu_env` ativado):

   ```bash
   python src/agents/edupersona-acompanhamento-desempenho.py
   ```

A aplicação estará pronta e em execução para interação via chat.
