# Foodgram, «Продуктовый помощник»

![Build Status](https://github.com/ipodjke/foodgram-project-react/actions/workflows/main.yml/badge.svg?branch=master)

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии

Список технологий используемых в проекте:

- [Django](https://www.djangoproject.com/) - Web framework
- [Django Rest FrameWork](https://www.django-rest-framework.org/) - is a powerful and flexible toolkit for building Web APIs
- [Gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server для UNIX
- [Docker](https://www.docker.com/) - Package Software into Standardized Units for Development, Shipment and Deployment
- [Nginx](https://nginx.org/ru/) - HTTP-сервер и обратный прокси-сервер, почтовый прокси-сервер, а также TCP/UDP прокси-сервер общего назначения
- [PostgreSQL](https://www.postgresql.org/) - база данных
- [ReactJS](https://reactjs.org) - фронтовая часть приложения

## Запуск

##### Возможны три варинта запуска проекта:

- запуск девовской версии.
    **Требования к запуску!:**
        Перед сборкой необходимо создать и заполнить файл /backend/envfiles/.env.dev,
        образец шаблона расположен /backend/envfiles/templates/env_base_template
        
    Особенности:
        - фронт и бэк функционируют отдельно друг от друга
        - доступен redoc с описанием api по адрессу api/docs/

```sh
cd infra
docker-compose up -d --build    
```

- запуск продовской версии для ручного разворачивания или дополнительного тестирования.
    **Требования к запуску!:**
        Перед сборкой необходимо создать и заполнить файл /backend/envfiles/.env.prod,
        образец шаблона расположен /backend/envfiles/templates/env_base_template
        
    Особенности:
        - все собирается в одно целое, для завершающего тестирования общей работоспособности проекта
        - не доступен redoc с описанием api по адрессу api/docs/

```sh
cd infra
docker-compose -f docker-compose.dev_b+f.yml up -d --build    
```

- запуск с помощью git hub actions.
    **Требования к запуску!:**
        Необходимо забить git hub secrets.
        
    Особенности:
        при пуше обновлений в master ветку, проводится тестирование, сборка образов, их заливка в докерхаб, далее подключение к серверу и развертывание проекта на нем.
        **Проект развертывается на основе docker-compose.prod.yml**

## Особенности

В папке дата находтся три файла:
- два со списком ингредиентов
- db.json базовый набор данных проекта


## Демо версия проекта

- host: http://62.84.122.150
- данные админа:
    - admin@admin.ru
    - admin
- пользователи:
    - test_{1..3}@mail.ru
    - 123456qwerty123456

## License

MIT

**Free Software, Hell Yeah!**