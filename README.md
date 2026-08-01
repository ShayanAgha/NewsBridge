<h1 align="center">
  <br>
  📰 NewsBridge
  <br>
</h1>

<p align="center">
  <b>A clean, self-hosted news aggregation platform powered by Flask</b><br>
  Receive articles from any source via Make.com — display them as a beautiful, searchable news feed.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Vercel-Deployed-000000?style=flat-square&logo=vercel&logoColor=white" alt="Vercel" />
  <img src="https://img.shields.io/badge/Make.com-Integration-6D00CC?style=flat-square&logo=integromat&logoColor=white" alt="Make.com" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
</p>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Make.com Integration](#-makecom-integration)
- [Deployment](#-deployment-vercel)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🗞️ Overview

**NewsBridge** is a lightweight, self-hosted news aggregation platform. It acts as the receiving end of an automated pipeline: an automation tool such as **Make.com** collects articles from RSS feeds or news APIs and pushes each one to NewsBridge via a simple JSON API. NewsBridge stores the articles and presents them as a polished, fully searchable news feed.

```
RSS Feed / News API / Any Source
             │
             ▼
      Make.com Scenario
  (fetch → map → filter)
             │
             │  POST /api/news  (JSON + Bearer token)
             ▼
    ┌─────────────────────┐
    │      NewsBridge      │
    │  validate · dedup   │
    │  store in SQLite    │
    └─────────────────────┘
             │
             ▼
    Public Website  /
    (search, filter, paginate)
```

---

## ✨ Features

### Public Site
| Feature | Details |
|---|---|
| **Homepage feed** | Featured story banner, latest-news ticker, article cards |
| **Search** | Full-text search across title, summary, and tags |
| **Filters** | Filter by category and source |
| **Sorting** | Newest, oldest, or most-viewed |
| **Pagination** | 12 articles per page |
| **Article page** | Image, summary, source link, related stories, tags, share buttons, view counter |

### Admin Area (`/admin`)
| Feature | Details |
|---|---|
| **Dashboard** | Article count, source stats, top articles |
| **Article management** | Search, publish/unpublish, delete |
| **Secure login** | Session-based authentication |

### API
| Feature | Details |
|---|---|
| **Ingest endpoint** | `POST /api/news` — receive articles from Make.com |
| **List endpoint** | `GET /api/news` — inspect up to 50 published articles as JSON |
| **Health check** | `GET /api/health` — uptime/deployment verification |
| **Deduplication** | Duplicate `source_url` values are silently accepted and never re-stored |

---

## 🏗️ Architecture

```
NewsBridge/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # SQLAlchemy Article model
│   ├── public_routes.py    # Public-facing pages (/, /article/<id>)
│   ├── admin_routes.py     # Admin dashboard & article management
│   ├── api_routes.py       # JSON API endpoints
│   ├── templates/
│   │   ├── base.html
│   │   ├── site/           # index.html, article.html
│   │   └── admin/          # login, dashboard, articles
│   └── static/
│       └── css/style.css
├── config.py               # Environment-aware configuration
├── run.py                  # Development entry point
├── wsgi.py                 # Production / Vercel entry point
├── vercel.json             # Vercel serverless configuration
├── requirements.txt
└── .env                    # Local secrets (never committed)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.1 |
| **Database** | SQLite (via Flask-SQLAlchemy) |
| **ORM** | Flask-SQLAlchemy 3.1 |
| **Config** | python-dotenv |
| **Automation** | Make.com (external) |
| **Hosting** | Vercel (serverless) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip`

### 1. Clone the repository

```bash
git clone https://github.com/ShayanAgha/NewsBridge.git
cd NewsBridge
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

> See [Environment Variables](#-environment-variables) for the full reference.

### 5. Run the development server

```bash
python run.py
```

Open **http://localhost:5000/** for the public news feed, or **http://localhost:5000/admin** for the admin panel.

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# Flask secret key — use a long random string
SECRET_KEY=replace-with-a-long-random-secret

# Bearer token used to authenticate POST /api/news requests
# Store ONLY the token — no "Bearer " prefix
API_BEARER_TOKEN=replace-with-a-long-random-secret

# Admin panel credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-me

# Set to "1" when running on Vercel (automatically set by Vercel)
# VERCEL=1
```

> ⚠️ **Important:** `API_BEARER_TOKEN` must contain **only** the raw secret, without the `Bearer ` prefix. Make.com sends `Authorization: Bearer <token>` — NewsBridge strips the prefix before comparing.

---

## 📡 API Reference

All API endpoints are prefixed with `/api`.

### `POST /api/news` — Ingest an article

**Authentication:** `Authorization: Bearer <API_BEARER_TOKEN>`

**Request body (JSON):**

| Field | Required | Description |
|---|---|---|
| `title` | ✅ | Article headline |
| `source_url` | ✅ | Canonical URL (used for deduplication) |
| `summary` | ❌ | Short excerpt shown in cards |
| `image_url` | ❌ | Publicly reachable image URL |
| `published_at` | ❌ | ISO-8601 datetime, e.g. `2026-07-27T12:30:00` |
| `source_name` | ❌ | Publisher / feed display name |
| `category` | ❌ | Defaults to `General` |
| `tags` | ❌ | Comma-separated string, e.g. `ai, startups` |

**Responses:**

| Status | Meaning |
|---|---|
| `201 Created` | Article saved successfully |
| `200 OK` | `source_url` already exists — safe to treat as success |
| `400 Bad Request` | Invalid JSON or missing required fields |
| `401 Unauthorized` | Missing or incorrect Bearer token |

---

### `GET /api/news` — List articles

**Authentication:** `Authorization: Bearer <API_BEARER_TOKEN>`

Returns up to 50 published articles as a JSON array, newest first.

---

### `GET /api/health` — Health check

No authentication required. Returns `{"status": "ok"}` with HTTP 200 when the application is running.

---

## ⚙️ Make.com Integration

### Scenario setup

1. **Source module** — Add an *RSS > Watch RSS feed items* module, or an *HTTP > Make a request* module pointing to your news API.
2. **Optional filter** — Add a Filter or Router to restrict by category, language, or date.
3. **HTTP module** — Send each item to NewsBridge.

### HTTP module settings

```
Method:      POST
URL:         https://YOUR-DOMAIN/api/news
Headers:
  Content-Type:   application/json
  Authorization:  Bearer YOUR_API_BEARER_TOKEN
Body type:   Raw (JSON)
```

### Example body

```json
{
  "title":        "{{feed title}}",
  "summary":      "{{feed description}}",
  "source_url":   "{{feed article link}}",
  "image_url":    "{{feed image URL}}",
  "published_at": "{{feed publication date}}",
  "source_name":  "{{feed or publisher name}}",
  "category":     "Technology",
  "tags":         "ai, startups, software"
}
```

---

## ☁️ Deployment (Vercel)

NewsBridge includes a ready-to-use `vercel.json`. Deployment is a single command:

```bash
vercel
```

Or connect the GitHub repository to Vercel and enable automatic deployments on push.

### Required Vercel environment variables

Set the following in your Vercel project settings under **Settings → Environment Variables**:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session secret |
| `API_BEARER_TOKEN` | API authentication token |
| `ADMIN_USERNAME` | Admin panel username |
| `ADMIN_PASSWORD` | Admin panel password |

> ⚠️ **Storage note:** On Vercel, SQLite is written to `/tmp/newsbridge.db` — a temporary, per-instance path. Articles may be lost when the serverless function is recycled. For a production workload, migrate to a managed database such as **PostgreSQL** (e.g., Neon, Supabase, or Vercel Postgres).

---

## 📂 Project Structure

```
NewsBridge/
├── app/
│   ├── __init__.py         # create_app() factory, DB init, blueprint registration
│   ├── models.py           # Article SQLAlchemy model
│   ├── public_routes.py    # Blueprint: public-facing pages
│   ├── admin_routes.py     # Blueprint: /admin routes
│   ├── api_routes.py       # Blueprint: /api routes
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── site/
│       │   ├── index.html
│       │   └── article.html
│       └── admin/
│           ├── base_admin.html
│           ├── login.html
│           ├── dashboard.html
│           └── articles.html
├── config.py
├── run.py
├── wsgi.py
├── vercel.json
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/ShayanAgha">ShayanAgha</a>
</p>
