# ИНТЕРВЬЮ БОТ
Бот для проведения опросов.

## <br><b>Тех.данные</b>
Бот построен на библиотеке python-telegram-bot

База данных используется MongoDB

## <br><b>Установка</b>

### <br><b>Откройте консоль</b>

<b>Выполните в консоли</b>             
    <details><summary> Команду: </summary>
```
git clone https://github.com/IgV52/tech_interiew_bot.git
```
</details>

### <br><b>Настройка</b>

<b>Создайте файл .env в каталоге tech_interiew_bot и добавьте туда следующие настройки:</b>
    <details>
    <summary> Параметры: </summary></b>
```

BOT_API = 'Ключ от BotFather'
ADMIN = (Telegram ID пользователя)
MONGO_LINK = 'Адрес базы данных'
MONGO_DB = 'Название базы данных'

PASSWORD_MAIL='Ключ приложения'
LOGIN_MAIL='Логин почты'
SEND_MAIL='Адрес почты для отправки'
SERVER_MAIL ='Сервер вашей почты'

```
</details>

## <br><b>Запуск</b>

<br><b>Зайдите в каталог tech_interiew_bot</b>

### <br><b>Откройте консоль</b>

<b>Выполните в консоли</b>             
    <details><summary> Команду: </summary>
```
docker-compose up --build
```
</details>
