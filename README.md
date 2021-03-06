# Тестовое задание для стажера в Market Intelligence
> *Cервис, позволяющий следить за изменением количества объявлений в Авито по определённому поисковому запросу и региону*

### Запуск
```bash
$ docker-compose up
```

### Добавление поискового запроса по региону в отслеживаемые
Принимает поисковой запрос по ключу `search_path`, регион по ключу `region`.
Пример тела запроса:
```json
{
  "search_path": "Бьёрн Страуструп С++",
  "region": "Москва"
}
```
```bash
$ curl --header "Content-Type: application/json" --request POST --data '{"search_path":"Бьёрн Страуструп С++","region":"Москва"}' http://localhost:8080/add/
```

### Просмотр истории счетчиков поискового запроса по id и интервалу
Принимает ключ `item_id`, выданный сервисом при добавлении, ключ `time_from` - дата , с которой нужно вывести счетчики, ключ `time_to` - дата, по которую нужно вывести счетчики. Формат даты - %Y-%m-%d:%H-%M. Все параметры с ключами передаются в гет параметрах запроса.
Пример пути: http://localhost:8080/stat/?item_id=1&time_from=2020-12-08:17-59&time_to=2020-12-10:15-00

### Просмотр истории топ 5 объявлений
Принимает ключ `item_id`, выданный сервисом при добавлении, ключ `time_from` - дата , с которой нужно вывести историю, ключ `time_to` - дата, по которую нужно вывести историю. Формат даты - %Y-%m-%d:%H-%M. Все параметры с ключами передаются в гет параметрах запроса.
Пример пути: http://localhost:8080/top/?item_id=1&time_from=2020-12-08:17-59&time_to=2020-12-10:15-00
