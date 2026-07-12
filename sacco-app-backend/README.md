# Sacco App — Group SACCO Savings Platform

Mobile-first web app for tracking member shares, treasurer verification, and admin governance.

Design language matches **E-voting-App-v2** (black / gold / cream, DM Serif Display + Source Sans 3).

---

## System architecture

```
┌─────────────────────┐     JWT      ┌──────────────────────────┐
│  Next.js (mobile    │◄────────────►│  Django REST Framework   │
│  web PWA-ready)     │   /api/*     │  accounts | savings |    │
│  src/app,components │              │  audit                   │
│  lib, styles        │              │  services layer          │
└─────────────────────┘              └────────────┬─────────────┘
                                                  │
                                         DATABASE_URL
                                                  ▼
                                         ┌────────────────┐
                                         │ Supabase       │
                                         │ Postgres       │
                                         └────────────────┘
```

**Layers (backend):** `models → serializers → services → views → urls`  
Business rules live in **services** only — views stay thin.

**Roles**

| Role | Capabilities |
|------|----------------|
| `super_admin` | Members, staff roles, all savings, audit, settings |
| `treasurer` | Verify/reject pending deposits, view all accounts |
| `secretary` | Member CRUD / verify members, read reports |
| `member` | Own balance, submit deposits (pending), history |

**Savings flow:** Member submits deposit → `pending` → Treasurer verifies → `verified` (balance += amount) or `rejected`.

---

## File structure

```
sacco-app-frontend/
  src/
    app/           # Next.js App Router pages
    components/    # Shared UI (Modal, BottomNav, …)
    lib/           # api.js, auth.js
    styles/        # globals.css (design system)
sacco-app-backend/
  sacco/           # Django project settings
  accounts/        # users, profiles, auth, staff/members
  savings/         # share accounts, transactions, verify
  audit/           # immutable audit trail
```

---

## Database schema (core)

- **User** — username, email, password, role, is_verified, is_active
- **MemberProfile** — member_number, phone, national_id, address, join_date
- **ShareAccount** — member (1:1), balance, total_shares
- **Transaction** — account, type, amount, status, reference, notes, submitted_by, verified_by, timestamps
- **AuditLog** — action, user_identifier, details, timestamp (+ indexes)

---

## API (prefix `/api`)

| Method | Path | Who |
|--------|------|-----|
| POST | `/accounts/login/staff/` | Staff |
| POST | `/accounts/login/member/` | Member (member_number) |
| POST | `/accounts/register/` | Public (pending verify) |
| GET | `/accounts/profile/` | Auth |
| GET/POST | `/accounts/members/` | Admin/secretary |
| POST | `/accounts/members/:id/verify/` | Admin/secretary |
| GET/POST | `/accounts/staff/` | Super admin |
| GET | `/savings/me/` | Member |
| GET | `/savings/accounts/` | Staff |
| GET/POST | `/savings/transactions/` | Role-scoped |
| POST | `/savings/transactions/:id/verify/` | Treasurer/admin |
| POST | `/savings/transactions/:id/reject/` | Treasurer/admin |
| GET | `/savings/dashboard/` | Staff |
| GET | `/audit/logs/` | Super admin / auditor-capable staff |

---

## UI architecture

- **Staff shell:** black topbar + sidebar (desktop), hamburger drawer (mobile) — same chrome as e-voting
- **Member shell:** black topbar + bottom tab bar (mobile-first)
- **Shared kit:** cards, stats, tables, badges, forms, login card on dark gold-stripe field

---

## Quick start

### Backend

```bash
cd sacco-app-backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # set DATABASE_URL for Supabase
python manage.py migrate
python manage.py seed_sacco
python manage.py runserver
```

### Frontend

```bash
cd sacco-app-frontend
npm install
npm run dev
```

Open http://localhost:3000 — default admin: `admin` / `admin123`

### Supabase

1. Create a Postgres project on [supabase.com](https://supabase.com)
2. Settings → Database → Connection string (URI)
3. Set `DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-….pooler.supabase.com:6543/postgres`
4. Prefer **Session mode** pooler for Django migrations; Transaction mode for app traffic if needed
5. Leave `DATABASE_URL` empty to use local SQLite

---

## Seed accounts

| Login | Password | Role |
|-------|----------|------|
| `admin` | `admin123` | super_admin |
| `treasurer` | `treasurer123` | treasurer |
| Member `SACCO0001` | `member123` | member |
