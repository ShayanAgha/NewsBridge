from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func

from app import db
from app.models import Article

public_bp = Blueprint('public', __name__)

ARTICLES_PER_PAGE = 12


@public_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    source = request.args.get('source', '').strip()
    sort = request.args.get('sort', 'newest')

    query = Article.query.filter_by(is_published=True)

    if search:
        query = query.filter(
            (Article.title.ilike(f'%{search}%')) |
            (Article.summary.ilike(f'%{search}%')) |
            (Article.tags.ilike(f'%{search}%'))
        )
    if category:
        query = query.filter(Article.category.ilike(f'%{category}%'))
    if source:
        query = query.filter(Article.source_name.ilike(f'%{source}%'))

    # coalesce avoids SQLite-incompatible NULLS LAST (breaks on Vercel)
    published_or_created = func.coalesce(Article.published_at, Article.created_at)

    if sort == 'oldest':
        query = query.order_by(published_or_created.asc())
    elif sort == 'popular':
        query = query.order_by(Article.views.desc())
    else:
        query = query.order_by(published_or_created.desc())

    pagination = query.paginate(page=page, per_page=ARTICLES_PER_PAGE, error_out=False)
    articles = pagination.items

    featured = Article.query.filter_by(is_published=True).order_by(Article.views.desc()).first()
    latest = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(5).all()
    trending = Article.query.filter_by(is_published=True).order_by(Article.views.desc()).limit(6).all()

    categories_raw = db.session.query(Article.category).filter(
        Article.is_published == True, Article.category.isnot(None)
    ).distinct().all()
    categories = sorted({c[0] for c in categories_raw if c[0]})

    sources_raw = db.session.query(Article.source_name).filter(
        Article.is_published == True, Article.source_name.isnot(None)
    ).distinct().all()
    sources = sorted({s[0] for s in sources_raw if s[0]})

    return render_template(
        'site/index.html',
        articles=articles,
        pagination=pagination,
        featured=featured,
        latest=latest,
        trending=trending,
        categories=categories,
        sources=sources,
        search=search,
        selected_category=category,
        selected_source=source,
        sort=sort,
    )


@public_bp.route('/article/<int:article_id>')
def article_detail(article_id):
    article = Article.query.filter_by(id=article_id, is_published=True).first_or_404()

    # Increment views
    article.views += 1
    db.session.commit()

    # Related articles: same category, exclude current
    related = Article.query.filter(
        Article.category == article.category,
        Article.id != article.id,
        Article.is_published == True
    ).order_by(func.coalesce(Article.published_at, Article.created_at).desc()).limit(4).all()

    return render_template('site/article.html', article=article, related=related)


@public_bp.route('/category/<category_name>')
def category(category_name):
    """Redirect category links into the filtered index view."""
    return redirect(url_for('public.index', category=category_name))
