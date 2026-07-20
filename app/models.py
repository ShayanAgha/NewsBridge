from datetime import datetime
from . import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    source_url = db.Column(db.String(1000), unique=True, nullable=False)
    image_url = db.Column(db.String(1000), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    source_name = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(100), nullable=True, default='General')
    tags = db.Column(db.String(500), nullable=True)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'source_url': self.source_url,
            'image_url': self.image_url,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'source_name': self.source_name,
            'category': self.category,
            'tags': self.tags,
            'views': self.views,
            'likes': self.likes,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
        }

    def get_tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    def reading_time(self):
        if self.summary:
            words = len(self.summary.split())
            minutes = max(1, round(words / 200))
            return minutes
        return 1

    def time_ago(self):
        """Return a human-readable time difference."""
        now = datetime.utcnow()
        ref = self.published_at or self.created_at
        diff = now - ref
        seconds = diff.total_seconds()
        if seconds < 60:
            return 'Just now'
        elif seconds < 3600:
            m = int(seconds // 60)
            return f'{m} minute{"s" if m > 1 else ""} ago'
        elif seconds < 86400:
            h = int(seconds // 3600)
            return f'{h} hour{"s" if h > 1 else ""} ago'
        elif seconds < 604800:
            d = int(seconds // 86400)
            return f'{d} day{"s" if d > 1 else ""} ago'
        else:
            return ref.strftime('%b %d, %Y')
