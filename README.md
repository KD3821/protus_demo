# protus_demo

<h1  align="center">PROTUS - система биллинга аккаунтов пользователей интернет-сервисов</h1>
<p align="center"><img src="https://img.shields.io/badge/made_by-KD3821-navy"></p><br>

<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic1.jpeg?raw=true"></p>

Функционал PROTUS:

Для Пользователя PROTUS:
<ul>
<li>Регистрация в сервисе PROTUS.</li>

<li>Попополнение баланса кошелька (в процессе... пока устанавливаем в БД).</li>

<li>Вход в партнерские интернет-сервисы (интегрированные с PROTUS), с помощью аккаунта PROTUS (по OAuth - выпускается только AccessToken и с возможностью ограничить scope для токена. Полный scope "check hold charge" - подразумевает доступ интернет-сервиса к проверке баланса кошелька, блокированию средств, списанию средств за услуги).</li>

<li>Просмотр состояния своих аккаунтов в различных интернет-сервисах (в этом цикле реализован только просмотр суммы расходов для каждого аккаунта).</li>
</ul>

Для Компании-партнера:
<ul>
<li>Регистрация компании и выдача ключа доступа к API, ключа для обработки входящих HTTP запросов на webhook компании-клиента.</li>

<li>Назначение WEBHOOK URL для запросов от PROTUS API (в процессе... пока устанавливаем в БД).</li>

<li>Регистрация услуги, для которой будет реализован биллинг аккаунтов пользователей (в процессе... пока устанавливаем в БД).</li>

<li>Биллинг аккаунтов непосредственных пользователей сервиса.</li>

<li>Просмотр состояния аккаунтов пользователей (в этом цикле реализован только просмотр суммы расходов для каждого аккаунта).</li>
</ul>

Для интеграции с сервисами-партнерами, реализованных на Django + DRF, разработан модуль PROTUS-DJANGO (пока модуль реализован как отдельный app 'protus' в демо-сервисе)
<ul>
<li>предоставляет свою систему JWT токенов (логика заимствована из модуля "djangorestframework-simplejwt")</li>
<li>предоставляет возможность пользователям PROTUS авторизоваться по OAuth в сервисе и оплачивать услуги с помощью кошелька PROTUS.</li>
<li>для непосредственных пользователей сервиса при первом входе регистрирует aккаунт + кошелек в PROTUS (требует кастомизации модели User - добавление полей uuid и oauth_verified)</li>
<li>предоставляет набор permissions, при добавлении которых к permission_classes для View-класса будет производится интроспекция токена для оаuth_verified пользователей (т.е. для пользователей, авторизованных с помощью PROTUS будет проверяться присутствие в scope токена нужных полей из списка "check hold charge", и что токен не был "отозван" на стороне PROTUS). Для непосредственных пользователей сервиса-клиента планируется, что набор scope будет максимальный для осуществления биллинга. Из permissions пока будет реализован ProtusChargePermission - проверяет наличие "charge" в scope токена, что позволяет списывать деньги с баланса кошелька пользователя PROTUS (oauth_verified). В данном цикле пополнение баланса PROTUS кошелька для непосредственных пользовтелей сервиса не будет реализовано.</li>
</ul>
<br>

<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic2.png?raw=true"></p>

Сервис PROTUS - это 3 микросервиса на FastAPI + модуль для Django(DRF):

<ul>
<li>GATEWAY (fast_gate)</li>
<li>AUTH (fast_auth)</li>
<li>PAYMENTS (fast_pay)</li>
<li>PROTUS-DJANGO (messages_app/protus) - оформление в модуль в процессе... в демо-приложении реализован как отдельный app 'protus'</li>
</ul>

Фронтенд PROTUS на Vue.js + Vuetify

MIRO: https://miro.com/app/board/uXjVKOFkZtk=/?share_link_id=649411215399

<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/miro.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic3.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic4.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic5.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic6.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic7.png?raw=true"></p>
<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/pic8.png?raw=true"></p>

Команды для запуска:
<ul>
<li>
Создайте .env файл в папках backend-приложений ('fast_auth', 'fast_gate', 'fast_pay', 'messages_app') - используйте данные из файлов env.example для каждого приложения.</li>
<li>
Перед запуском docker-compose из консоли установите пароль для POSTGRES в переменную среды командой: export POSTGRES_PASSWORD=Billing123 (ваш пароль должен совпадать с паролями в .env файле - используем общий пароль).</li>
<li>
Также измените дефолтное значение таймаута для HTTP-соединения у контейнеров в момент сборки - из консоли запустите команду: export COMPOSE_HTTP_TIMEOUT=600 (вместо 60 сек. - 600 сек. либо больше).</li>
<li>
Запустите команду в консоли: docker-compose -f docker-compose.yml up --build (дождитесь завершения сборки сети контейнеров).</li>
<li>
Если по какой-то причине процесс остановился с ошибкой - вызовите команду из консоли: docker-compose down и дождитесь остановки. Затем повторите предыдущий шаг.</li>
<li>
</ul>
<br>
Для Django приложения: войдите в контейнер backend-messages ( sudo docker exec -it backend-messages /bin/bash -c "su - root" ) и выполнить:
<p>cd /code/</p>
<p>python manage.py createsuperuser</p>
<p>авторизуйтесь в Django Admin ( http://127.0.0.1:8000/admin ) и установите 'IntervalSchedule' для Celery Beat: 5, 10, 30 секунд (три интервала) - подробности работы django-приложения см. <a href="https://github.com/KD3821/message_service" target="_blank">тут</a></p><br>

Для Payments приложения: войти в контейнер backend_protus_pay ( sudo docker exec -it backend_protus_pay /bin/bash -c "su - root" ) и выполнить:
<p>cd /app/src/</p>
<p>alembic revision --autogenerate -m "initial on build"  (создаем миграции и таблицы БД)</p>
<p>alembic upgrade head</p>
<p>python -m proto.grpc_server &  (запускаем gRPC сервер)</p><br>

Для Auth приложения: войти в контейнер backend_protus_auth ( sudo docker exec -it backend_protus_auth /bin/bash -c "su - root" ) и выполнить:
<p>cd /app/src/</p>
<p>alembic revision --autogenerate -m "initial on build"  (создаем миграции и таблицы БД)</p>
<p>alembic upgrade head</p>
<p>python -m proto.grpc_server &  (запускаем gRPC сервер)</p><br>


Демонстрация работы:
<ul>
<li>
Переходим на сайт сервиса PROTUS (http://127.0.0.1:8080) и регистрируем компанию в сервисе "PROTUS" (любые данные).</li>
<li>
Подключаемся к БД 'fast_auth_db' (БД для AUTH-приложения) и меняем сгенерированные 'CLIENT_ID', 'CLIENT_SECRET', 'WH_SECRET' на свои из.env в messages_app (чтобы не перезапускать docker-compose).</li>
<li>
Заполняем данные для 'WH_URL': "/api/webhook/" (для POST-запросов от PROTUS-сервиса).</li>
<li>
Повторяем все для 'fast_pay_db' (БД для PAYMENTS-приложения).</li>
<li>
Добавляем две услуги в таблице services в 'fast_pay_db' (Можно назвать их "Клиент", "Рассылка" - цены любые) - для service_id используем данные из.env в messages_app (чтобы не перезапускать docker-compose).</li>
<li>
Далее регистрируем пользователя - при желании можно в БД 'fast_pay_db' прописать баланс его кошелька в таблице 'wallets' (при регистрации баланс равен 0 - игнорируем поля 'debit', 'credit' - они пока не задействованы в логике).</li>
<li>
Переходим на сайт компании-партнера (http://127.0.0.1:8088) и входим в сервис через "вход с PROTUS" разрешив все действия для Access Token.</li>
<li>
Далее пользуемся сервисом - соглашаемся оплатить услуги по добавлению нового клиента и по запуску рассылок (подробнее о работе сервиса компании партнера см. <a href="https://github.com/KD3821/message_service" target="_blank">тут</a>.</li>
<li>
Проверяем на сайте PROTUS в ЛК Компании и Пользователя списания средств.</li>
<li>
Далее проверяем логику работы биллинга для обычного пользователя сервиса компании-партнера: регистрируем на сайте партнера нового пользователя - получаем услуги - проверяем в ЛК компании на сайте PROTUS создание аккаунта и биллинг.</li>
<li>
Для запуска сервиса можно обратиться за консультацией.</li>
</ul>

<p align="center"><img src="https://github.com/kd3821/protus_demo/blob/main/img/dori.jpeg?raw=true"></p>
