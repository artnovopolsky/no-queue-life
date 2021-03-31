# Welcome to NoQueueLife!

NoQueueLife – это сервис, позволяющий пользователю найти человека, который отстоит за него в любой очереди. Популярные запросы к сервису подразумевают очередь за модной обувью, билетами на концерт и, конечно же, за новыми гаджетами.


## Features

* Будет
* обновлено 
* позже.

## Getting started

В дальнейшем приложение можно будет установить через pip, пока для сборки и развертывания поступаем так:

```
git clone https://github.com/artnovopolsky/no-queue-life.git
cd no-queue-life
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Documentation

Чтобы ознакомиться с документацией проекта, перейдите в терминале в директорию `docs/` и введите:

```
sphinx-autobuild . ./_build/html
```

Документация будет сгенерирована автоматически и доступна локально по адресу http://127.0.0.1:8000/.
