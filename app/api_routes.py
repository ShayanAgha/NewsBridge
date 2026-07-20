from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models import Article
from datetime import datetime

api_bp = Blueprint('api', __name__)


def verify_token():
    """Verify the Bearer token from the Authorization header."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split('Bearer ', 1)[1].strip()
    return token == current_app.config['API_BEARER_TOKEN']


@api_bp.route('/news', methods=['POST'])
def create_news():
    """
    POST /api/news
    Accepts article data from Make.com, validates token, checks duplicates,
    and saves to database.

    Expected JSON body:
    {
        "title": "...",
        "summary": "...",
        "source_url": "...",
        "image_url": "...",
        "published_at": "2024-01-01T12:00:00",
        "source_name": "...",
        "category": "...",   (optional)
        "tags": "..."        (optional, comma-separated)
    }
    """
    # 1. Authenticate
    if not verify_token():
        return jsonify({'status': 'error', 'message': 'Unauthorized. Invalid or missing Bearer token.'}), 401

    # 2. Parse JSON body
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON body.'}), 400

    # 3. Validate required fields
    title = (data.get('title') or '').strip()
    source_url = (data.get('source_url') or '').strip()

    if not title or not source_url:
        return jsonify({'status': 'error', 'message': 'Missing required fields: title and source_url must be non-empty strings.'}), 400

    # 4. Check for duplicate
    existing = Article.query.filter_by(source_url=source_url).first()
    if existing:
        return jsonify({'status': 'already_exists', 'id': existing.id}), 200

    # 5. Parse published_at date
    published_at = None
    if data.get('published_at'):
        for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S %z'):
            try:
                dt = datetime.strptime(str(data['published_at'])[:19], fmt[:len(str(data['published_at'])[:19])])
                published_at = dt.replace(tzinfo=None)
                break
            except (ValueError, TypeError):
                continue

    # 6. Create and save article
    article = Article(
        title=title,
        summary=(data.get('summary') or '').strip() or None,
        source_url=source_url,
        image_url=(data.get('image_url') or '').strip() or None,
        published_at=published_at,
        source_name=(data.get('source_name') or '').strip() or None,
        category=(data.get('category') or 'General').strip() or 'General',
        tags=(data.get('tags') or '').strip() or None,
    )

    db.session.add(article)
    db.session.commit()

    return jsonify({'status': 'created', 'id': article.id}), 201


@api_bp.route('/news', methods=['GET'])
def list_news():
    """GET /api/news — Returns all published articles as JSON (useful for testing)."""
    if not verify_token():
        return jsonify({'status': 'error', 'message': 'Unauthorized.'}), 401

    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(50).all()
    return jsonify({'status': 'ok', 'count': len(articles), 'articles': [a.to_dict() for a in articles]}), 200


@api_bp.route('/health', methods=['GET'])
def health():
    """GET /api/health — Public health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'NewsBridge API is running.'}), 200
