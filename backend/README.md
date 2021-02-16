## Backend - Análises de dados de passageiros

Este backend serve para armazenar os dados de estudo em um banco de dados, gerenciado pela ORM do Django e disponibilizá-los ao frontend por meio de uma API desenvolvida pela biblioteca Django Rest Framework.

### Testando Localmente


Lembre-se de verificar se o terminal está na pasta `backend` para que seja possível realizar as operações seguintes.

```system
$ cd backend
```

#### para rodar pela primeira vez:

1. Instale o Python;
2. Instale as dependências:

```system
$ pip install -r requirements.txt
```

3. Instale o PostgreSQL;

4. Crie um banco de dados no PostegreSQL;

5. Crie um arquivo `conf/secret.py` com as seguintes informações:

```python
SECRET_KEY = 'Sua_chave_secreta'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<NOME DO BANCO>', # Nome do banco que você criou no PostgreSQL no passo acima.
        'USER': '<SEU USUÁRIO>', # Seu usuário Postgres
        'PASSWORD': 'SENHA', # Sua senha Postgres
        'HOST': 'localhost', 
        'PORT': '5432',
    }
}
```

6. Atualize o banco de dados:

```system
$ python manage.py migrate
```

7. Crie um usuário admin:

```system
$ python manage.py createsuperuser
```
7. Crie um objeto funcionário no admin e associar ao seu usuário;



#### Para rodar o servidor local (É necessário toda vez que for testar a aplicação)

```system
$ python manage.py runserver
```