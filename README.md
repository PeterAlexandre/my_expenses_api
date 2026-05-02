# my-expenses-api

Personal finance management API. Helps organize monthly finances by tracking income and expenses, categorizing transactions, and generating monthly reports.

## Stack

- **Python 3.13** + **FastAPI**
- **PostgreSQL** via **SQLAlchemy 2.0**
- **Alembic** for migrations
- **JWT** authentication (OAuth2 password flow)
- **Docker Compose** for the database

## Getting started

**1. Start the database**
```bash
docker-compose up -d
```

**2. Install dependencies**
```bash
uv sync
```

**3. Configure environment**

Copy `.env` and adjust if needed:
```bash
cp .env .env.local
```

Required variables:
```
DATABASE_URL=postgresql://expenses_user:expenses_password@localhost:5432/expenses_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**4. Run migrations**
```bash
alembic upgrade head
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/token` | — | Login, returns JWT |
| POST | `/account` | — | Register user |
| GET | `/account` | ✓ | Get current user |
| PATCH | `/account` | ✓ | Update current user |
| DELETE | `/account` | ✓ | Delete current user |
| POST | `/transactions` | ✓ | Create transaction |
| GET | `/transactions` | ✓ | List transactions (filterable) |
| GET | `/transactions/{id}` | ✓ | Get transaction |
| PATCH | `/transactions/{id}` | ✓ | Update transaction |
| DELETE | `/transactions/{id}` | ✓ | Delete transaction |
| POST | `/categories` | ✓ | Create category |
| GET | `/categories` | ✓ | List categories |
| GET | `/categories/{id}` | ✓ | Get category |
| PATCH | `/categories/{id}` | ✓ | Update category |
| DELETE | `/categories/{id}` | ✓ | Delete category |
| GET | `/reports/monthly` | ✓ | Monthly financial report |

### Transaction filters

`GET /transactions` accepts optional query params:

| Param | Values | Description |
|-------|--------|-------------|
| `type` | `income`, `expense` | Filter by type |
| `status` | `done`, `provision` | Filter by status |
| `payment_method` | `credit_card`, `account` | Filter by payment method |
| `category_id` | integer | Filter by category |
| `month` | 1–12 | Filter by month |
| `year` | 2000+ | Filter by year |

### Monthly report

`GET /reports/monthly?year=2026&month=05`

Defaults to the current month. Returns:
- **summary** — total income, total expenses, difference
- **credit_card_total** — total credit card charges
- **current_balance** — done income minus done account expenses
- **by_category** — expense breakdown with percentages
- **provisions** — pending income and expenses with totals

## Category pattern matching

Categories support automatic assignment via patterns. When creating a transaction without a `category_id`, the API checks all user categories with a pattern and assigns the first match.

Patterns are case-insensitive substrings. Multiple patterns per category are separated by `;`:

```
"netflix;nflx;streaming"
```

If a `category_id` is explicitly provided on the transaction, pattern matching is skipped.

## Development

**Run migrations after model changes:**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Lint and format:**
```bash
ruff check .
ruff format .
```

**Run tests:**
```bash
pytest
```
