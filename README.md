
# Публикация комиксов с сайте xkcd.com в группе vk.com
Скрипт загружает изображение случайного комикса с сайта [xkcd](https://xkcd.com/) и публикует его на стене в паблике [Вконтакте](https://vk.com/).

[API xkcd](https://xkcd.com/json.html)  
[Выполнение запросов к API ВКонтакте](https://vk.com/dev/api_requests)
## Подготовка
1.  При необходимости  [создать паблик Вконтакте](https://vk.com/groups?tab=admin).
2.  Получить  [идентификатор группы](https://regvk.com/id/).
3.  В разделе "Мои приложения"  [страницы для разработчиков](https://vk.com/dev)  создать  _standalone-приложение_.
4.  Получить  `client_id`  созданного приложения (кнопка  _Редактировать_).
5.  Получить личный ключ (`access_token`) для доступа приложения к личному аккаунту:
    -   использовать процедуру  [Implicit Flow](https://vk.com/dev/implicit_flow_user);
    -   убрать параметр  `redirect_uri`  у запроса на ключ;
    -   параметр  `scope`  указать с необходимыми разрешениями:  `scope=photos, groups, wall, offline`.
    -   при запросе браузер будет перенаправлен на страницу, в адресной строке которой находится личный ключ доступа (параметр  `access_token`).  
        _Пример_:  `533bacf01e1165b57531ad114461ae8736d6506a3`
        
## Установка и запуск

Python3 должен быть уже установлен. 
1. Клонируйте репозиторий
```
https://github.com/rudenko-ks/web-api-xkcd-to-vk.git
```
2. Создайте виртуальное окружение
```
python -m venv .venv
source .venv/bin/activate
```
3. Используйте `pip` (или `pip3`, если конфликт с Python2) для установки зависимостей
```
pip install -r requirements.txt
```
4. Создайте файл `.env` с переменными окружения. Пример:
```
VK_ACCESS_TOKEN=<YOUR ACCESS TOKEN>
VK_GROUP_ID=<GROUP ID IN VK.COM>
```
5. Запустите скрипт
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков  [dvmn.org](https://dvmn.org/).