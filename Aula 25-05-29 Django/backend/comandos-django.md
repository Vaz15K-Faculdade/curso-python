# Comandos Django

### Antes de tudo...
Crie uma pasta para seu projeto e abra com o Visual Studio Code (VSCode).

### Instalação (todo sistema)
```
pip install django
```

### Instalação pipenv
De dentro da pasta do seu projeto rode:
```
pipenv install django
```
isso irá instalar o Django em um ambiente virtual e criar dois novos arquivos:
```
pasta_projeto\
    Pipfile
    Pipfile.lock
```

Opcional (caso o VSCode não detectar automaticamente): Após isso selecione o interpretador Python do ambiente virtual com as teclas `Ctrl`+`Shift`+`p` e digite `Select Interpreter` ou `Selecionar Interpretador` caso seu VSCode esteja em Português, por fim, **selecione a opção que possui o nome da pasta do projeto**. 

### Criando um novo projeto
Utilizando o terminal do VSCode de dentro da pasta criada para o projeto rode o comando:
```
django-admin startproject nome_do_seu_projeto .
```
Isso irá criar uma pasta com o nome do seu projeto e um arquivo `manage.py`:
```
pasta_projeto\
    manage.py
    nome_do_seu_projeto\
        ...
```

### Criar aplicação:
```
python manage.py startapp app
```

### Rodar Aplicação:
```
python manage.py runserver
```

### Aplicar migrações do banco de dados (sempre que houver alteração nos models)
```
python manage.py makemigrations
python manage.py migrate
```

### Criar usuário admin
```
python manage.py createsuperuser
```