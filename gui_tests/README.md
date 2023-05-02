# Application

## Развертывание
1. Возвращаемся в root dir (test_task)
`cd ..`
2. Собираем контейнеры
`docker-compose -f staging-local.docker-compose.yml build`
3. Запустить контейнеры 
`docker-compose -f staging-local.docker-compose.yml up -d`
4. Вернуться в текущую директорию (gui_tests)
`cd gui_tests`
5. Развернуть виртуальное окружение
`python3 -m venv venv`
6. Активировать окружение
- MacOS / Linux
- - `source venv/bin/activate`
- MS
- - `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- - `.venv\Scripts\Activate.ps1`
7. Установить все модули
`pip install -r requirements.txt`
8. Запустить тесты
`pytest`
