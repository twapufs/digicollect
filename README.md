# DigiCollect

DigiCollect — веб-приложение для коллекционирования цифровых карточек. Администраторы создают карточки с заданным количеством экземпляров, а коллекционеры забирают их себе, пока тираж не закончится.

## Стек

Бэкенд написан на Python с FastAPI и хранит данные в PostgreSQL через SQLAlchemy. Для хэширования паролей используется Argon2, аутентификация — JWT. Фронтенд написан на React с TypeScript, Vite, Tailwind CSS и DaisyUI. Взаимодействие с API построено на Axios и TanStack Query. В продакшене всё собирается через Docker Compose: PostgreSQL, FastAPI-сервер и Nginx, который раздаёт собранный фронтенд и проксирует запросы к API.

## Структура проекта

```
digicollect/
  client/       фронтенд на React + Vite
  server/       бэкенд на FastAPI
  docker-compose.yml
  .env.example
```

Бэкенд внутри разбит на слои:

- `api/` — FastAPI-роутеры, схемы запросов и ответов, зависимости
- `application/` — сервисы с бизнес-логикой
- `domain/` — сущности, value objects, абстрактные репозитории, доменные исключения
- `infrastructure/` — SQLAlchemy-модели, конкретные реализации репозиториев, Unit of Work
- `core/` — конфигурация и утилиты безопасности

## API

Базовый путь: `/api/v1`

Аутентификация:
- `POST /auth/register` — регистрация (поле `role`: `collector` или `admin`; для `admin` нужен `admin_key`)
- `POST /auth/token` — получение JWT-токена (form data: `username`, `password`)

Пользователи:
- `GET /users/me` — информация о текущем пользователе

Карточки (мастер-копии):
- `GET /master-cards/` — список всех карточек
- `GET /master-cards/{id}` — одна карточка
- `POST /master-cards/` — создать карточку (только админ)
- `PATCH /master-cards/{id}` — изменить карточку (только админ)
- `DELETE /master-cards/{id}` — удалить карточку (только админ)

Коллекция:
- `GET /collection/` — моя коллекция
- `POST /collection/` — забрать карточку (тело: `master_card_id`)
- `DELETE /collection/{id}` — вернуть карточку из коллекции

## Локальный запуск бэкенда

Требуется Python 3.12+ и [uv](https://docs.astral.sh/uv/).

```
cd server
uv sync
uv run uvicorn main:app --reload
```

По умолчанию сервер использует SQLite (`local.db`) и стартует на `http://localhost:8000`. Переменные окружения можно задать через файл `server/.env`:

```
DATABASE_URL=sqlite:///local.db
JWT_SECRET_KEY=change-me
ADMIN_REGISTRATION_KEY=change-me-admin-key
```

## Локальный запуск фронтенда

Требуется Node.js 18+.

```
cd client
npm install
npm run dev
```

Фронтенд запустится на `http://localhost:5173` и будет обращаться к серверу на `http://localhost:8000`.

## Тесты

Фаззинг-тесты для бэкенда находятся в `server/tests/`. Они проверяют поведение API при некорректных, граничных и неожиданных входных данных.

```
cd server
uv run pytest tests/ -q
```

Тесты используют отдельную SQLite-базу (`test_fuzz.db`), которая создаётся и удаляется автоматически.
