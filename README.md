# Edupersona
## Sistema multiagente BDI para orientação personalizada de alunos via chat inteligente

Este projeto utiliza o framework [SPADE](https://spadeagents.eu/) para criar um sistema multiagente que oferece orientação personalizada para alunos através de um chat inteligente.

## Instalação

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

4.  **Inicie o servidor XMPP:**
    ```bash
    spade run
    ```

5.  **Execute o agente:**
    ```bash
    python simple-agent.py
    ```
