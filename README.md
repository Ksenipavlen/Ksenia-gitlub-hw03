# Домашнее задание 2: кластеризация и балансировка нагрузки

В этом репозитории реализованы две задачи по настройке HAProxy для балансировки нагрузки между Python-серверами.

## Структура проекта

- `configs/task1-haproxy.cfg` — конфигурация HAProxy для задачи 1
- `configs/task2-haproxy.cfg` — конфигурация HAProxy для задачи 2
- `scripts/start-task1.sh` — запуск Python-серверов для задачи 1
- `scripts/start-task2.sh` — запуск Python-серверов для задачи 2
- `run/` — PID-файлы запущенных процессов
- `logs/` — лог-файлы (если создаются)

---

## Задание 1 — балансировка TCP на уровне 4

### Цель
Настроить HAProxy для балансировки TCP-запросов между двумя Python-серверами.

### Конфигурация
Файл: `configs/task1-haproxy.cfg`

```haproxy
defaults
    mode tcp

backend task1_python_servers
    mode tcp
    balance roundrobin
    server py1 127.0.0.1:8001
    server py2 127.0.0.1:8002
```

### Запуск
В одном терминале запустите сервисы Python:

```bash
./scripts/start-task1.sh
```

В другом терминале проверьте конфигурацию HAProxy и запустите его:

```bash
haproxy -c -f configs/task1-haproxy.cfg
sudo haproxy -f configs/task1-haproxy.cfg
```

### Проверка
Отправьте несколько запросов к HAProxy:

```bash
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/
```

Ожидаемый результат: ответы должны чередоваться между `task1-py1` и `task1-py2`.

Пример:

```text
server=task1-py1
port=8001

server=task1-py2
port=8002
```

### Скриншоты

![Задание 1 результат 1](https://github.com/user-attachments/assets/2d544323-1096-4d0d-99ae-597b44c360cf)

![Задание 1 результат 2](https://github.com/user-attachments/assets/4eac6f84-04bd-4656-a167-adeb1a1962bf)

---

## Задание 2 — балансировка HTTP на уровне 7 с ACL по Host

### Цель
Настроить HAProxy для HTTP-балансировки с проверкой заголовка `Host` и распределением запросов между тремя серверами с разными весами.

### Конфигурация
Файл: `configs/task2-haproxy.cfg`

```haproxy
frontend task2_http_front
    bind *:8081
    mode http
    acl host_example hdr(host) -i example.local example.local:8081
    http-request deny deny_status 403 unless host_example
    use_backend task2_python_servers if host_example

backend task2_python_servers
    mode http
    balance roundrobin
    server py1 127.0.0.1:8011 weight 2
    server py2 127.0.0.1:8012 weight 3
    server py3 127.0.0.1:8013 weight 4
```

### Запуск
В одном терминале запустите Python-сервера:

```bash
./scripts/start-task2.sh
```

В другом терминале проверьте конфигурацию HAProxy и запустите его:

```bash
haproxy -c -f configs/task2-haproxy.cfg
sudo haproxy -f configs/task2-haproxy.cfg
```

### Настройка локального домена
Если проверка выполняется на той же машине, добавьте домен `example.local` в `/etc/hosts`:

```bash
echo "127.0.0.1 example.local" | sudo tee -a /etc/hosts
```

### Проверка
Отправьте несколько запросов к HAProxy с использованием домена:

```bash
for i in {1..18}; do curl -s http://example.local:8081/ | grep '^server='; done
```

Ожидаемое распределение за 18 запросов:
- `task2-py1` примерно 4 раза
- `task2-py2` примерно 6 раз
- `task2-py3` примерно 8 раз

Проверка запроса без правильного Host:

```bash
curl -i http://127.0.0.1:8081/
```

Ожидаемый результат: ответ `403 Forbidden` для запроса без заголовка `Host: example.local`.

### Скриншоты

![Задание 2 результат 1](https://github.com/user-attachments/assets/f2872752-73ed-4233-9081-8e02ad50f81f)

![Задание 2 результат 2](https://github.com/user-attachments/assets/71761d35-45ea-49bb-b0b8-572b38323a1a)

![Задание 2 результат 3](https://github.com/user-attachments/assets/d80c1f45-2cb6-4dac-b9aa-164a7fde19df)

---

## Примечания

- Все команды запуска предполагают, что вы находитесь в корневой папке репозитория.
- Если `sudo haproxy -f ...` запрашивает пароль, введите пароль пользователя для выполнения команды от имени root.
- `REPORT.md` объединён в этот `README.md` и дополнительный отчёт не требуется.




