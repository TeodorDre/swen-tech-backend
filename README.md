# swen.tech.backend
## Backend системы разметки

### http-service

### DataBase
В настоящий момент используется тестовая БД, запущенаня в Docker-контейнере, основанном на latest-версии postgres

### Bootstrap
sql-код находится в файле `/bootstrap/sql/`

Так же реализован бутстрап на базе моделей ORM, однако при таком подходе не реализуется создание полей типа `timestamptz`

`migrations.py` запускается с аргументом
В настоящий момент реализован только бутстрап

``` -sh
$python migrations.py  bootstrap | migration
```

### Dummy Data
Находится в файле dummy_data.py и запускаются без аргумента.

``` -sh
$python dummy_data.py
```

### Пример config.yml
```
postgres:
  host: localhost
  port: 5432
  user: markup
  database: markup
  password: markup
logger:
  logger_level: DEBUG
  format: '[{asctime}][{levelname}] - {name}: {message}'
  style: '{'
app:
  port:
    8080
s3:
  accesskeyid: your_key
  secret_access_key: your_secret
  bucket: target_bucket
  region: eu-central-1
```