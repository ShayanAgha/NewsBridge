# Automated News Aggregator Website (Flask + Make.com)

This project is an **automated news aggregation platform** where news articles are collected from multiple RSS feeds using **Make.com**, stored in a database through a **Flask REST API**, and displayed on a modern, responsive website. The goal is to demonstrate **web development, REST API development, database management, authentication, and workflow automation**.

---

# 1. Public Website (Frontend)

## 🏠 Home Page

* Latest news articles
* Featured news section
* Breaking news ticker
* Trending news section
* News cards with image, title, summary, source, and publication date
* Responsive design

---

## 📰 Article Details Page

* Full article information
* Featured image
* Source name
* Published date
* Estimated reading time
* "Read Original Article" button
* Related articles section
* Share buttons (Facebook, X, LinkedIn, WhatsApp)

---

## 🔍 Search

* Search by title
* Search by keywords
* Live search suggestions

---

## 📂 Categories

Examples:

* Technology
* Business
* Sports
* Entertainment
* Health
* Science
* World

---

## 🏷 Tags

Articles can contain tags such as:

* AI
* Python
* Space
* Microsoft
* Apple

Clicking a tag displays related articles.

---

## 📡 Filter Options

* Filter by news source
* Filter by category
* Filter by date
* Filter by latest/trending

---

## 📅 Sorting

* Newest First
* Oldest First
* Most Viewed
* Most Recent Imports

---

## 📄 Pagination

Display articles page by page.

---

## ❤️ User Features

* Bookmark articles
* Like articles
* Comment on articles (optional)
* User registration/login (optional)
* User profile
* Saved articles

---

## 🌙 UI Features

* Dark Mode
* Grid/List view
* Responsive design
* Lazy loading images
* Placeholder image when RSS has no image
* "Published X minutes ago"

---

# 2. Admin Panel

## 🔐 Admin Login

Secure administrator authentication.

---

## 📊 Dashboard

Display statistics such as:

* Total articles
* Articles imported today
* Total RSS sources
* Articles per category
* Most viewed article
* Latest imported article
* Duplicate articles skipped

---

## 📝 Article Management

* View articles
* Edit articles
* Delete articles
* Publish/Unpublish articles

---

## 📡 RSS Feed Management

* Add RSS feed
* Remove RSS feed
* Enable/Disable feeds
* View feed status

*(RSS URLs can still be stored in Google Sheets for the assignment, but this is a useful future enhancement.)*

---

## 📜 Import History

Track every Make.com import:

* Date & time
* Feed name
* Number of imported articles
* Duplicates skipped
* Status (Success/Failed)

---

## 🚫 Source Blacklist

Disable unwanted RSS feeds without deleting them.

---

# 3. Flask REST API

This is the core integration point with Make.com.

## POST `/api/news`

Accepts:

* title
* summary
* source_url
* image_url
* published_at
* source_name
* category (optional)
* tags (optional)

---

## Security

* HTTPS only
* Bearer Token authentication
* API key validation

---

## Duplicate Protection

Uses `source_url` as a unique identifier.

If the article already exists:

```json
{
    "status":"already_exists"
}
```

Otherwise:

```json
{
    "status":"created",
    "id":125
}
```

---

# 4. Database

### News Table

* id
* title
* summary
* image_url
* source_url (Unique)
* source_name
* published_at
* category
* tags
* views
* likes
* created_at

---

# 5. Make.com Automation

## Workflow

```
Google Sheets
      │
      ▼
RSS Feed URLs
      │
      ▼
Make.com Scheduler
      │
      ▼
Retrieve RSS Articles
      │
      ▼
Extract Article Data
      │
      ▼
POST Request
/api/news
      │
      ▼
Flask API
      │
      ├── Validate Token
      ├── Validate Data
      ├── Check Duplicate
      ├── Save to Database
      └── Return Response
      │
      ▼
Website Updates Automatically
```

---

# 6. Automation Features

These features highlight the use of Make.com.

* Automatic RSS feed collection
* Automatic article publishing
* Duplicate prevention
* Automatic image handling via image URLs
* Scheduled imports (e.g., every hour)
* Daily import reports
* Email notifications for new imports
* Telegram notifications
* Social media posting (Facebook, X, LinkedIn)
* Error alerts if RSS feeds fail
* Approval workflow (Pending → Approved → Published)

---

# 7. Analytics & Monitoring

## Analytics Dashboard

* Total articles
* Total sources
* Daily imports
* Weekly imports
* Monthly imports
* Most active RSS source
* Most viewed articles
* Articles by category

---

## RSS Feed Health Dashboard

* Feed online/offline status
* Last synchronization time
* Number of imported articles
* Success rate
* Failed imports
* Duplicate count

---

## Live Import Activity

Display recent automation events, such as:

* "10:30 AM — BBC: 5 articles imported"
* "10:35 AM — CNN: 2 duplicates skipped"
* "10:40 AM — TechCrunch: Import successful"

---

## Import Queue Monitor

Show the current automation status:

* Waiting
* Importing
* Completed
* Failed

---

# 8. Performance & UX

* Responsive design (Desktop, Tablet, Mobile)
* Lazy loading images
* Fast page loading
* Pagination
* Caching
* Progressive Web App (PWA) support (optional)

---

# 9. Optional Advanced Features

* Interactive world map showing news by country
* News timeline view
* Source reliability badges
* Trending news based on views
* Featured news carousel
* Daily "Top Stories" section
* Newsletter subscription
* RSS feed export
* Multi-language support
* Weather widget or stock ticker (optional)

---

# Technologies Used

### Frontend

* HTML5
* CSS3
* Bootstrap 5 (or Tailwind CSS)
* JavaScript

### Backend

* Flask (Python)
* Flask REST API

### Database

* SQLite (development)
* MySQL (production)

### Automation

* Make.com
* Google Sheets
* RSS Feeds

### Authentication

* Bearer Token / API Key

### Version Control

* Git & GitHub

---

# Core Workflow

```
Google Sheets (RSS Feed URLs)
           │
           ▼
       Make.com
           │
           ▼
   Retrieve RSS Articles
           │
           ▼
 Extract Article Information
           │
           ▼
   Flask REST API (/api/news)
           │
           ├── Authenticate Request
           ├── Validate Fields
           ├── Prevent Duplicates
           ├── Save to Database
           └── Return JSON Response
           │
           ▼
       Database (MySQL/SQLite)
           │
           ▼
   News Website Updates Automatically
           │
           ▼
Users Read, Search, Filter, Bookmark, and Share News
```

## Recommended Scope for Your Semester Project

To create a polished, realistic, and achievable project, focus on these **must-have features**:

### Core Features

* ✅ Responsive homepage with featured, latest, trending, and breaking news
* ✅ Individual article pages
* ✅ Search, filtering, sorting, and pagination
* ✅ Categories and tags
* ✅ Secure admin login and dashboard
* ✅ Article management (view, edit, delete, publish/unpublish)
* ✅ Secure Flask REST API with Bearer token authentication
* ✅ Duplicate detection using `source_url`
* ✅ Automatic RSS import through Make.com
* ✅ Import history and RSS feed health dashboard
* ✅ Clean, professional UI

### Optional Features (Time Permitting)

* ⭐ Bookmarks and likes
* ⭐ Comments
* ⭐ Dark mode
* ⭐ Newsletter subscription
* ⭐ Social media auto-posting
* ⭐ Email/Telegram notifications
* ⭐ Interactive news map
* ⭐ Progressive Web App (PWA)

This feature set demonstrates software engineering concepts including **web development, database design, REST APIs, authentication, automation with Make.com, analytics dashboards, and responsive UI/UX**, making it a comprehensive and impressive semester project.
