# Picpay Desafio Engineer

Este projeto consiste de uma aplicação Web desenvolvido com FastAPI. A principal finalidade dele são a disponibilidade das operações de CRUD (GET, POST, PUT, DELETE) para a entidade "User/Usuário", garantindo seus testes unitários como também a qualidade e estrutura do código.

## Pré-requisitos

### Python

Certifique-se de ter o Python instalado na sua máquina. Você pode verificar se o Python está instalado executando o seguinte comando no terminal:

```bash
python --version
```

## Instruções de Uso

1. Clone este repositório para a sua máquina:

   ```bash
   git clone https://github.com/renanreyc/picpay_desafio_engineer.git
   ```
2. Navegue até o diretório clonado:

    ```bash
    cd seu-repositorio
    ```

3. Criação de ambiente de Desenvolvimento:
   ```bash
    python -m venv venv
    ```

4. Instalação de dependências listadas no `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

5. Para inicialização da aplicação, execute o seguinte comando de acordo com seu sistema operacional:

- Windows:
    ```bash
    fastapi dev .\\src\\app.py
    ```
- Linux/IOS:
    ```bash
    fastapi dev src/app.py
    ```

6. Após a inicialização, você pode acessar a interface da aplicação no endpoint  [localhost](http://127.0.0.1:8000), como também sua documentação em [docs](http://127.0.0.1:8000/docs).

(importante!) No endereço de documentação há toda a documentação necessária para acesso, testes e consumo da aplicação.

## Testes e Ambiente de Desenvolvimento

1. Para ambiente de desenvolvimento e realização de testes. instale também as dependências em `requirements-dev.txt`

    ```bash
    pip install -r requirements-dev.txt
    ```

    você pode iniciar a aplicação executando `task run` ou executar os tests com `task test` editando as paths no arquivo `pyproject.toml` de acordo com seu Sistema Operacional.

---


Desenvolvido por Renan Rey :lobster:
