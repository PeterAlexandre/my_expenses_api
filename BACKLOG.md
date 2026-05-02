# Backlog

## In progress / next up

### CSV import
Import credit card bills from bank-exported CSV files.
- Parse CSV and bulk-create transactions
- Auto-assign categories via pattern matching on import
- Skip duplicates (same description + amount + date)
- Return a summary: how many imported, how many skipped

---

## Planned

### Tests
The test suite is currently minimal (one JWT test). Needs coverage for:
- Auth flow (login, invalid credentials, expired token)
- Transaction CRUD and ownership isolation
- Category CRUD and pattern matching logic
- Monthly report calculations

### Pagination
`GET /transactions` currently returns all transactions with no limit.
Add `page` and `page_size` query params and return total count in response.

### Refresh tokens
Access tokens currently expire and the user must log in again.
Add a refresh token endpoint so sessions can be extended without re-entering credentials.

---

## Ideas (not yet decided)

### Recurring transaction auto-generation
Transactions marked `is_recurring=True` could be automatically projected into the next month as `provision` entries, pre-populating the monthly view.

### Budget limits per category
Set a monthly spending limit on a category and surface it in the report (spent vs limit, percentage used).

### Frontend — React
Separate repository. Planned views:
- Monthly dashboard (bar graph for income vs expenses, pie chart for categories)
- Transaction list with filters
- Category management
- CSV import UI

Deploy: API as Docker container, React app as static files (Vercel or self-hosted Nginx).

---

## Done

- [x] User registration and authentication (JWT)
- [x] Transaction CRUD with filtering by type, status, payment method, category, month, year
- [x] Per-user categories with pattern-based auto-assignment
- [x] Multi-pattern support per category (semicolon-separated)
- [x] Monthly report: summary, credit card total, current balance, category breakdown, provisions
- [x] Alembic migrations
