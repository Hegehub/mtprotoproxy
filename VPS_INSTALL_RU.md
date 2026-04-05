# Установка и запуск MTProto Proxy на VPS (с «чистой» системы)

> Ниже — практичная инструкция для **нового/переустановленного VPS**.
> 
> Если под «очисткой до заводских» вы имеете в виду полный сброс сервера, делайте это через панель вашего провайдера (**Reinstall OS / Rescue / Rebuild**). Это безопаснее и надежнее, чем вручную удалять системные пакеты на рабочей ОС.

## 0) Что подготовить заранее

- Доступ в панель VPS-провайдера.
- SSH-доступ (пароль root или SSH-ключ).
- Домен не обязателен.
- Открытый порт (по умолчанию `3256`, можно изменить).

Рекомендуемая минимальная конфигурация:
- 1 vCPU
- 1 GB RAM
- 10+ GB диска
- Ubuntu 22.04/24.04 LTS

---

## 1) Полная очистка VPS до «заводского» состояния

1. Зайдите в панель провайдера.
2. Найдите действие типа:
   - **Reinstall OS**
   - **Rebuild**
   - **Reset / Factory reset**
3. Выберите свежую ОС (лучше `Ubuntu 22.04 LTS` или `Ubuntu 24.04 LTS`).
4. Подтвердите переустановку.
5. Дождитесь завершения и получите новый IP/пароль (или подтвердите SSH-ключ).

> ⚠️ Все данные на сервере будут удалены.

---

## 2) Первичный вход и базовая подготовка

Подключитесь по SSH:

```bash
ssh root@YOUR_SERVER_IP
```

Обновите систему:

```bash
apt update && apt -y upgrade
```

(Опционально) настройте часовой пояс:

```bash
timedatectl set-timezone UTC
```

---

## 3) Установка Docker и Docker Compose Plugin

Установите зависимости:

```bash
apt install -y ca-certificates curl gnupg
```

Добавьте официальный репозиторий Docker:

```bash
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Установите Docker Engine и Compose:

```bash
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Проверьте:

```bash
docker --version
docker compose version
```

---

## 4) Установка MTProto Proxy

Клонируйте репозиторий:

```bash
git clone -b stable https://github.com/Hegehub/mtprotoproxy.git
cd mtprotoproxy
```

Создайте env-файл из шаблона:

```bash
cp .env.example .env
nano .env
```

Минимально проверьте/измените:
- `PORT` — порт прокси (например, `443`)
- `USERS` — список секретов в формате `имя:секрет`
- `AD_TAG` — рекламный тег (опционально)

> Секреты в `USERS` должны быть длинными и случайными (32 hex-символа).

---

## 5) Запуск

Запуск в фоне:

```bash
docker compose up -d --build
```

Проверка статуса:

```bash
docker compose ps
```

Логи:

```bash
docker compose logs -f --tail=100
```

---

## 6) Открытие порта в firewall

Если используете UFW:

```bash
ufw allow OpenSSH
ufw allow 443/tcp
ufw --force enable
ufw status
```

Если вы поменяли `PORT` в `.env`, откройте именно его.

Также убедитесь, что порт разрешен в **cloud firewall/security group** у вашего провайдера.

---

## 7) Автозапуск после перезагрузки

Обычно Docker сам стартует. Проверьте:

```bash
systemctl enable docker
systemctl status docker --no-pager
```

Контейнер из `docker compose up -d` должен подниматься автоматически (политика рестарта уже задана в compose).

---

## 8) Обновление прокси

```bash
cd ~/mtprotoproxy
git pull
docker compose up -d --build
```

---

## 9) Полезные команды для диагностики

```bash
# Проверка, что порт слушается
ss -lntp | grep 443

# Статус контейнеров
docker compose ps

# Последние логи
docker compose logs --tail=200
```

---

## 10) Быстрый чек-лист

- [ ] VPS переустановлен через панель провайдера
- [ ] Установлен Docker + Docker Compose Plugin
- [ ] Склонирован `stable`-бранч репозитория
- [ ] Настроен `.env`
- [ ] Выполнен `docker compose up -d`
- [ ] Открыт порт прокси в UFW и в cloud firewall
- [ ] Проверены логи

Готово: прокси работает на вашем VPS с «чистой» системы.
