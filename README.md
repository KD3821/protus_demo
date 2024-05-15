# protus_demo

<h1  align="center">PROTUS - система биллинга аккаунтов пользователей интернет-сервисов</h1>

Функционал PROTUS:

Для Пользователя PROTUS:
<ul>
<li>1. Регистрация в сервисе PROTUS.</li>

<li>2. Попополнение баланса кошелька (в процессе...)</li>

<li>3. Вход в партнерские интернет-сервисы (интегрированные с PROTUS),  с помощью аккаунта PROTUS (по OAuth - выпускается только AccessToken и с возможностью ограничить scope для токена. Полный scope "check hold charge" - подразумевает доступ интернет-сервиса к проверке баланса кошелька, блокированию средств, списанию средств за услуги)</li>

<li>4. Просмотр состояния своих аккаунтов в различных интернет-сервисах (в этом цикле реализован только просмотр суммы расходов для каждого аккаунта)</li>
</ul>

Для Компании-партнера:
<ul>
<li>1. Регистрация компании-клиента и выдача ключа доступа к API, ключа для обработки входящих HTTP запросов на webhook компании-клиента</li>

<li>2. Назначение WEBHOOK URL для запросов от PROTUS API</li>

<li>3. Регистрация услуги, для которой будет реализован биллинг аккаунтов пользователей</li>

<li>4. Биллинг аккаунтов непосредственных пользователей сервиса</li>

<li>5. Просмотр состояния аккаунтов пользователей своего интернет-сервиса (в этом цикле реализован только просмотр суммы расходов для каждого аккаунта)</li>
</ul>

Для интеграции с сервисами-партнерами, реализованных на Django + DRF, разработан модуль PROTUS-DJANGO (пока модуль реализован как отдельный app 'protus'в демо-сервисе)
<ul>
<li>- предоставляет свою систему JWT токенов (логика взаимствована из модуля "djangorestframework-simplejwt")</li>
<li>- предоставляет возможность пользователям PROTUS авторизовываться по OAuth в сервисе и получать платные услуги, оплачивая их с помощью кошелька PROTUS.</li>
<li>- для непосредственных пользователей сервиса при первом входе регистрирует aккаунт + кошелек в PROTUS (требует кастомизации модели User - добавление полей uuid и oauth_verified)</li>
<li>- предоставляет набор permissions - при добавлении к списку permission_classes у View class во время запроса к нему производится интроспекция токена для оаuth_verified пользователей (т.е. для пользователей, авторизованных с помощью PROTUS - проверяется присутствие в scope токена нужных полей "check hold charge" и что токен не был "отозван" на стороне PROTUS). Для непосредственных пользователей сервиса-клиента планируется, что набор scope будет максимальный для осуществления биллинга. Из permissions пока будет реализован ProtusChargePermission - проверяет наличие "charge" в scope токена, что позволяет списывать деньги с баланса кошелька пользователя PROTUS (oauth_verified). В данном цикле пополнение баланса PROTUS кошелька для непосредственных пользовтелей сервиса не будет реализовано.</li>
</ul>

Сервис PROTUS - это три микросервиса на FastAPI:

- GATEWAY
- AUTH
- PAYMENTS

Фронт PROTUS на Vue.js + Vuetify

MIRO: https://miro.com/app/board/uXjVKOFkZtk=/?share_link_id=649411215399


#######################################

Команды для запуска: docker-compose up -d --build

в контейнере backend_protus_pay ( sudo docker exec -it backend_protus_pay /bin/bash -c "su - root" )
cd /app/src/
alembic revision --autogenerate -m "initial on build"
alembic upgrade head
python -m proto.grpc_server &



в контейнере backend_protus_auth ( sudo docker exec -it backend_protus_auth /bin/bash -c "su - root" )
cd /app/src/
alembic revision --autogenerate -m "initial on build"
alembic upgrade head
python -m proto.grpc_server &