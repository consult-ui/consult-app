# consult-app server

это тебе не кисловодс братишка и не есентуки, это, вася, лайнер, круизный лайнер


*Запускаем проект с Docker:*

1. Создать файл .env.local 
2. Поинтересоваться о содержимом для данного файла 
3. Выполнить docker-compose -f docker-compose.local.yaml up -d --build

*Запустить тесты без Docker:*
1. Создать и активировать виртуальное окружение 
2. Установить зависимости из requirements.txt
3. python -m pytest -s -vv --alluredir=allure-results
4. allure serve 

Перед запуском тестов необходимо установить allure server: <https://allurereport.org/docs/install/>
Для запуска в CI можно использовать документацию: <https://allurereport.org/docs/integrations-github/>
