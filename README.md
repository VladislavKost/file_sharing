# Структура проекта
1. Для авторизации и регистрации пользователей используется библиотека dj-rest-auth. Некоторые сериализаторы и вью переписаны для корректной работы.
2. Для расширения модели User была создана новая модель CustomUser в приложении accounts.
3. Для работы с файловым хранилищем создано приложение files_store. 
4. Для аутентификации пользователя используется JWT.

Для задания параметров нужно создать файл .env в корне проекта и записать в него:
SECRET_KEY=your_secret_key
DEBUG=True/False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5174
FRONTEND_URL=http://localhost:5174
#Database data
DB_NAME=your_db_name
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=your_user
DB_PASSWORD=your_password
