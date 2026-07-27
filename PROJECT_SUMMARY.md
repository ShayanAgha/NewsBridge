# NewsBridge Project Summary

## Purpose

NewsBridge is a Flask-based news aggregation website. It does **not** fetch RSS feeds or news-provider APIs itself. Instead, an automation tool such as Make.com collects articles from one or more sources and sends each article to NewsBridge. NewsBridge stores the article, then displays it as a searchable news feed on the website.

## What is implemented

- Public news homepage with a featured story, latest-news ticker, article cards, category/source filters, search, sorting, and pagination (12 articles per page).
- Individual article pages with image, summary, source link, related stories, tags, sharing links, and a view counter.
- Admin area for login, dashboard statistics, article search, publish/unpublish, and deletion.
- SQLite storage with duplicate prevention based on `source_url`.
- JSON API for receiving articles from Make.com and returning stored articles for testing or another consumer.
- Vercel configuration and a health-check endpoint.

## How the news feed works

```text
RSS feed / News API / website source
             |
             v
       Make.com scenario
  (read, map, optionally filter)
             |
             | POST one article as JSON
             v
      NewsBridge POST /api/news
  (authenticate, validate, deduplicate, save)
             |
             v
          SQLite database
             |
             v
   NewsBridge public website (/)
```

1. Make.com reads an RSS feed or a news-provider API on a schedule.
2. It maps each feed item to the JSON fields accepted by `POST /api/news`.
3. NewsBridge validates the request and stores the article unless that exact `source_url` already exists.
4. The public homepage queries published articles and renders them in the feed. Newly imported content appears on the next page load.
5. Clicking a card opens NewsBridge's article page; the **Read Full Article** button opens the original publisher URL.

## APIs required

NewsBridge itself requires **one incoming integration API call per article**:

| API endpoint | Authentication | Use |
| --- | --- | --- |
| `POST /api/news` | Bearer token | Required: receive an article from Make.com |
| `GET /api/news` | Bearer token | Optional: inspect up to 50 published articles as JSON |
| `GET /api/health` | None | Optional: deployment/uptime health check |

For content sources, Make.com needs at least **one** source connection. This can be an RSS module (often no API key) or a news-provider API such as NewsAPI, GNews, or a publisher-specific API (normally an API key). The number of external source APIs depends on how many independent feeds/providers you want to import; it is not fixed by this code.

## Make.com setup

Create a scheduled scenario with these modules:

1. **Source module:** RSS > Watch RSS feed items, or an HTTP module calling your chosen news API.
2. **Optional filter/deduplication:** only send relevant categories, language, or recent items. NewsBridge also prevents duplicates by `source_url`.
3. **HTTP > Make a request:** send each item to NewsBridge.

Use the following HTTP request settings:

```text
Method: POST
URL: https://YOUR-DOMAIN/api/news
Header: Content-Type: application/json
Header: Authorization: Bearer YOUR_SECRET_TOKEN
Body type: Raw / JSON
```

Example JSON body (map the values from the preceding Make.com module):

```json
{
  "title": "{{feed title}}",
  "summary": "{{feed description or excerpt}}",
  "source_url": "{{feed article link}}",
  "image_url": "{{feed image URL}}",
  "published_at": "{{feed publication date}}",
  "source_name": "{{feed or publisher name}}",
  "category": "Technology",
  "tags": "ai, startups, software"
}
```

### Field rules

| Field | Required | Notes |
| --- | --- | --- |
| `title` | Yes | Non-empty article headline |
| `source_url` | Yes | Original article URL; it is unique and prevents duplicate imports |
| `summary` | No | Short article excerpt shown in cards and article pages |
| `image_url` | No | Publicly reachable image URL |
| `published_at` | No | Prefer an ISO-8601 date such as `2026-07-27T12:30:00` |
| `source_name` | No | Publisher/feed display name |
| `category` | No | Defaults to `General` |
| `tags` | No | Comma-separated text, for example `world, politics` |

### Expected responses

- `201 Created` with `{"status":"created","id":123}`: article saved.
- `200 OK` with `{"status":"already_exists","id":123}`: source URL was already imported; this is safe to treat as success.
- `400 Bad Request`: JSON or the required `title`/`source_url` is invalid.
- `401 Unauthorized`: Authorization header/token is incorrect.

## Important configuration note before connecting Make.com

The current token check removes `Bearer ` from the request header and compares the remaining secret to `API_BEARER_TOKEN`. Therefore, the environment variable must contain **only the secret**, without the `Bearer ` prefix:

```env
API_BEARER_TOKEN=replace-with-a-long-random-secret
```

Then Make.com sends:

```text
Authorization: Bearer replace-with-a-long-random-secret
```

The current `.env.example` includes `Bearer ` in the variable value, which would cause valid Make.com requests to receive `401 Unauthorized` unless that value is changed (or the authentication code is adjusted). Change the default admin password and secret key as well before deployment.

## How results are displayed

- `GET /` shows only articles where `is_published` is true, newest first by `published_at` (falling back to import time).
- Visitors can search title, summary, and tags; filter by category/source; and sort newest, oldest, or most viewed.
- Each article has a NewsBridge detail page at `/article/<id>`. Opening that page increments its view count.
- The admin area at `/admin` can hide or delete imported articles. Hidden articles remain in the database but do not appear publicly or in the API list.

## Deployment/storage consideration

Local development uses `instance/newsbridge.db`. On Vercel the application uses `/tmp/newsbridge.db`, which is temporary serverless storage. It is appropriate for a demo but not reliable for a production feed because imported articles can disappear when the serverless instance is replaced. For a durable production integration, move the database to a managed persistent database (for example PostgreSQL) and configure its connection string.

## Local run and verification

```bash
pip install -r requirements.txt
python run.py
```

Then open `http://localhost:5000/` for the public feed or `http://localhost:5000/api/health` to verify the application is running.

