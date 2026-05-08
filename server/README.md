# DigiCollect — Server

FastAPI backend for a trading card collecting app. Admins create master cards with a fixed print run; collectors add copies to their personal collection.

---

## Architecture

Clean / DDD layering. Dependencies point inward — infrastructure knows about domain, domain knows nothing about infrastructure.

```
server/
├── domain/           # Entities, value objects, domain exceptions, abstract repositories & UoW
├── application/      # Use-case services, application exceptions
├── infrastructure/   # SQLAlchemy ORM models, concrete repositories, UoW implementation
├── api/              # FastAPI routers, Pydantic schemas, dependency wiring
└── core/             # Settings (pydantic-settings), security utilities (JWT, Argon2)
```

---

## Domain

### Value objects

| Type | Values |
|------|--------|
| `Role` | `admin` · `collector` |
| `Rarity` | `common` · `uncommon` · `rare` · `epic` · `legendary` |

### Entities

**`User`** — `username`, `hashed_password`, `role`, `id`
Methods: `is_admin()`, `is_collector()`, `update_username/password/role()`

**`MasterCard`** — `title`, `symbol` (unicode), `rarity`, `description`, `quantity`, `available_quantity`, `id`
Methods: `can_collect()`, `collect()`, `return_card()`, `update_*()`, `update_quantity()` — enforces quantity can never fall below already-collected count.

**`CollectedCard`** — `master_card`, `user`, `collected_at`, `id`
`CollectedCard.create(master_card, user)` calls `master_card.collect()` internally, enforcing availability.
`collected_card.remove()` calls `master_card.return_card()`, restoring one slot.

### Domain exceptions

`CardNotAvailableError` · `InvalidQuantityError` · `InsufficientPermissionsError`

---

## Application services

Each service receives an open `AbstractUnitOfWork` and calls `uow.commit()` itself. Authorization is enforced at the service boundary via the actor's role.

| Service | Operations |
|---------|------------|
| `UserService` | `register` · `login` → JWT · `authenticate` token → `User` |
| `MasterCardService` | `create` · `get` · `list_all` · `update` (partial) · `delete` — admin only |
| `CollectedCardService` | `collect` · `remove` · `list_my_collection` — collector only |

### Application exceptions

`UserAlreadyExistsError` · `InvalidCredentialsError` · `InvalidTokenError` · `TokenExpiredError` · `MasterCardNotFoundError` · `CollectedCardNotFoundError`

---

## Infrastructure

- **ORM**: SQLAlchemy 2 declarative models (`UserModel`, `MasterCardModel`, `CollectedCardModel`). `CollectedCardModel` holds FK columns; relationships are loaded explicitly with `selectinload` in queries.
- **Repositories**: one per aggregate (`SqlAlchemyUserRepository`, `SqlAlchemyMasterCardRepository`, `SqlAlchemyCollectedCardRepository`). Each maps between ORM model ↔ domain entity.
- **Unit of Work**: `SqlAlchemyUnitOfWork` opens a session on `__enter__`, exposes all three repositories sharing that session, rolls back on unhandled exceptions.
- **DB init**: `build_session_factory(url, init_db=True)` runs `Base.metadata.create_all` on startup when `AUTO_DB_INIT=true` (default). Suitable for SQLite dev; use Alembic migrations for production.

---

## Security

| Concern | Implementation |
|---------|---------------|
| Password hashing | Argon2 via `argon2-cffi` (`PasswordHasher`) |
| Tokens | HS256 JWT via `PyJWT`; claims: `sub` (user UUID), `iat`, `exp` |
| Auth flow | OAuth2 Password Bearer — POST `/api/v1/auth/token` returns `access_token` |

---

## API

Base path: `/api/v1`

### Auth

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/token` | — | Login; returns `{ access_token, token_type }` |
| `POST` | `/auth/register` | — | Register new user; returns `UserResponse`. Registering as `admin` requires `admin_key` in the request body. |

### Users

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/users/me` | Bearer | Current user profile |

### Master cards (admin only)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/master-cards/` | admin | Create master card |
| `GET` | `/master-cards/` | admin | List all master cards |
| `GET` | `/master-cards/{id}` | admin | Get master card by ID |
| `PATCH` | `/master-cards/{id}` | admin | Partial update |
| `DELETE` | `/master-cards/{id}` | admin | Delete → 204 |

### Collection (collector only)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/collection/` | collector | Collect a card (`{ master_card_id }`) |
| `GET` | `/collection/` | collector | List own collected cards |
| `DELETE` | `/collection/{id}` | collector | Return a card → 204 |

### HTTP error codes

| Code | When |
|------|------|
| 401 | Missing, expired, or invalid token |
| 403 | Authenticated but wrong role · invalid or missing admin registration key |
| 404 | Entity not found |
| 409 | Username taken · no copies of card available |
| 422 | Invalid quantity (below already-collected count) |

---

## Configuration

Environment variables (or `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///test.db` | SQLAlchemy connection string |
| `JWT_SECRET_KEY` | `change-me-in-production` | HMAC signing key |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime |
| `AUTO_DB_INIT` | `true` | Run `create_all` on startup |
| `ADMIN_REGISTRATION_KEY` | `change-me-admin-key` | Secret key required in the request body to register with role `admin` |

---

## Running

```bash
cd server
uv run uvicorn main:app --reload
```

Interactive docs available at `http://localhost:8000/docs`.
