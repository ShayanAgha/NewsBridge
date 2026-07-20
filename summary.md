### Project Summary

Your project is an **automated news website** built with **Flask (Python)** and **Make.com**.

**How it works:**

1. Store RSS feed URLs in **Google Sheets**.
2. **Make.com** reads those RSS feeds on a schedule.
3. It extracts article details:

   * Title
   * Summary
   * Source URL
   * Image URL
   * Published Date
   * Source Name
4. Make.com sends this data to your **Flask API** using an **HTTP POST** request.
5. Your Flask API:

   * Verifies the API token (security).
   * Checks if the article already exists using `source_url`.
   * Saves the article to the database if it's new.
   * Returns a success or "already exists" response.
6. Your website displays all saved articles from the database.

### What you need to build

* A **News** database table.
* A **POST API endpoint** (e.g., `/api/news`) to receive articles from Make.com.
* **API authentication** (Bearer token or API key).
* **Duplicate protection** using `source_url`.
* A webpage to display the stored news articles.

### Overall Workflow

```text
Google Sheets (RSS URLs)
        ↓
     Make.com
        ↓
  Reads RSS Feeds
        ↓
 Extracts Articles
        ↓
POST /api/news
        ↓
    Flask API
        ↓
Validate Token
Check Duplicates
Save to Database
        ↓
   News Website
```

In short, **Make.com automates collecting news**, and **your Flask application provides the secure API and website that stores and displays those news articles**.
