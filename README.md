сайт Foodgram, «Продуктовый помощник». 
Реализация онлайн API при готовом frontnend
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд
REST API реализовано на django и django-rest-framework
Docker Образ проет автоматически деплоится на сервер с помощью git actions,
и автоматически разворачивается на сервере.
Взаимодействие backend и frontend происходит через сервер nginx.
Посмотреть можно по ссылке https://foodgramm.myddns.me/
Можно развернуть этот проект на любом сервере, для этого необходимо
1) Скопировать содержимое папки infra на ваш сервер.
2) Выполнить команду sudo docker-compose-up
3) Создать суперпользователя: sudo docker exec -it geo_web_1 createsuperuser

Альтернативный вариант:
Выполнить Fork контейнера,
Из GitHub Actions удалить build_and_push_to_docker_hub
В переменных Secrets указать
HOST - IP сервера 
USER - имя пользователя 
SSH_KEY - приватный ключ для доступа к вашему серверу
Поместить в Secrets содержимое файла .env
проект задеплоится при выполнении push на GitHub

![example workflow](https://github.com/GEORGELIZGIN/foodgram-project-react/actions/workflows/foodgram_workflow/badge.svg)
