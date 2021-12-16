# Foodgram, «Продуктовый помощник»

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Суть

Данный проект был разработан в учебных целях, а так же попробовать использовать DDD совместно с Django
> [DDD django styly guid](https://phalt.github.io/django-api-domains/files/#services) - This styleguide combines domain-driven design principles and Django's apps pattern to provide a pragmatic guide for developing scalable API services with the Django web framework

## Расширении style guide и другие умозкалючения

- в папке utils определен базовый класс для реализации логики service, который основан не GenereicViewSet, который позволяет
сохранить основные фишки Django Rest FrameWork(pagination, фильтрацию).
- управление доступа к REST api осуществляется из соображений доступ к API(has_permission) осуществляется в файлах api.py,
а доступ к объектам(has_object_permission) осуществляется в services.py
- относительно serializers.py это как прослойка между service и models, и по ххорошему все управление моделью нужно осуществлять
через него, но метода delete нету, что ведет к мысли о необходимости расширения поведение сереализатора, но целесообразность данного действия необходимо обдумывать
- в API не используется ModelViewSet так как его методы обходят services.py и на прямую взаимодействуют с моделями приложения,
что запрещено в рамках данного гида
- возможно стоит более очевидно разделять бизнес логику отдающую ответ REST API и внутрених интерфейсов приложение т.е REST API
возвращает JSON, а внутренние API приложений отдавать QuerySet, но в данном приложении внутренние API приложений так же отдают 
JSON

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

- запуск девовской версии для тестирования и отладки взаимодействия фронта и бека.
    **Требования к запуску!:**
        Перед сборкой необходимо создать и заполнить файл /backend/envfiles/.env.dev_b+f,
        образец шаблона расположен /backend/envfiles/templates/env_base_template
        
    Особенности:
        - все собирается в одно целое, для завершающего тестирования общей работоспособности проекта
        - не доступен redoc с описанием api по адрессу api/docs/
        - доступен redoc с описанием api по адрессу api/docs/
        - доступны порты как nginx(80) так и бэкенда(8080)

```sh
cd infra
docker-compose -f docker-compose.dev_b+f.yml up -d --build    
```

- запуск с помощью git hub actions.
    **Требования к запуску!:**
        Необходимо заполнить git hub secrets.
        
    Особенности:
        при пуше обновлений в master ветку, проводится тестирование, сборка образов, их заливка в докерхаб, далее подключение к серверу и развертывание проекта на нем.
        **Проект развертывается на основе docker-compose.prod.yml**

## Демо версия проекта

```sh
cd infra
docker-compose -f docker-compose.dev_b+f.yml up -d --build    
```
- данные админа:
   - создаются из /backend/envfiles/.env.dev_b+f
   - зайти в контейнер бекенда и с помощью manage.py createsuperuser

## License

MIT

**Free Software, Hell Yeah!**
