from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Article
from config import Config
from datetime import datetime, timedelta
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        cfg = Config()
        if username == cfg.ADMIN_USERNAME and password == cfg.ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_articles = Article.query.count()
    published_articles = Article.query.filter_by(is_published=True).count()
    today = datetime.utcnow().date()
    today_articles = Article.query.filter(
        func.date(Article.created_at) == today
    ).count()

    # Articles per category
    categories_data = db.session.query(
        Article.category, func.count(Article.id)
    ).group_by(Article.category).all()

    # Most viewed
    most_viewed = Article.query.order_by(Article.views.desc()).first()

    # Latest import
    latest_import = Article.query.order_by(Article.created_at.desc()).first()

    # Import history: last 7 days
    import_history = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = Article.query.filter(func.date(Article.created_at) == day).count()
        import_history.append({'date': day.strftime('%b %d'), 'count': count})

    # Sources stats
    sources_data = db.session.query(
        Article.source_name, func.count(Article.id)
    ).group_by(Article.source_name).order_by(func.count(Article.id).desc()).limit(8).all()

    return render_template(
        'admin/dashboard.html',
        total_articles=total_articles,
        published_articles=published_articles,
        today_articles=today_articles,
        categories_data=categories_data,
        most_viewed=most_viewed,
        latest_import=latest_import,
        import_history=import_history,
        sources_data=sources_data,
    )


@admin_bp.route('/articles')
@login_required
def articles():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '')

    query = Article.query
    if search:
        query = query.filter(Article.title.ilike(f'%{search}%'))
    if status_filter == 'published':
        query = query.filter_by(is_published=True)
    elif status_filter == 'unpublished':
        query = query.filter_by(is_published=False)

    pagination = query.order_by(Article.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    articles_list = pagination.items
    return render_template('admin/articles.html', articles=articles_list, pagination=pagination, search=search, status_filter=status_filter)


@admin_bp.route('/articles/<int:article_id>/toggle', methods=['POST'])
@login_required
def toggle_article(article_id):
    article = Article.query.get_or_404(article_id)
    article.is_published = not article.is_published
    db.session.commit()
    return redirect(url_for('admin.articles'))


@admin_bp.route('/articles/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('admin.articles'))
