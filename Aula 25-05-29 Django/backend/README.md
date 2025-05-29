# Backend do projeto em Django

### Instalar Django (pipenv)
De dentro da pasta `backend` rode para instalar as bibliotecas utilizadas:
```
pip install --user pipenv
python -m pipenv install
```

Para entrar no ambiente virtual:
```
pipenv shell
```

### Criar nova aplicação
```
python manage.py startapp nome_do_app
```

### Rodar aplicação:
```
python manage.py runserver
```

### Aplicar migrações do banco de dados (sempre que houver alteração nos models)
```
python manage.py makemigrations
python manage.py migrate
```

### Criar usuário administrador
```
python manage.py createsuperuser
```