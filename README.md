# swen.tech.backend

### Bootstrap
sql-код находится в файле `/bootstrap/sql/`

`migrations.py` запускается с аргументом
В настоящий момент реализован только бутстрап

``` -sh
$python migrations.py  bootstrap | migration
```

### Dummy Data

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