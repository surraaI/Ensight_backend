from sqlalchemy.orm import Session
from app.models.article import Article, ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate
from sqlalchemy import select, update

class ArticleService:
    @staticmethod
    def get_articles_by_category(db: Session, category: str):
        return db.execute(
            select(Article).filter_by(category=category, status=ArticleStatus.PUBLISHED)
        ).scalars().all()

    @staticmethod
    def get_articles_by_subcategory(db: Session, category: str, subcategory: str):
        return db.execute(
            select(Article).filter_by(category=category, subcategory=subcategory, status=ArticleStatus.PUBLISHED)
        ).scalars().all()

    @staticmethod
    def get_article_by_slug(db: Session, category: str, subcategory: str, slug: str):
        return db.execute(
            select(Article).filter_by(category=category, subcategory=subcategory, slug=slug, status=ArticleStatus.PUBLISHED)
        ).scalar_one_or_none()

    @staticmethod
    def get_article_by_id(db: Session, article_id: str):
        return db.execute(select(Article).filter_by(id=article_id)).scalar_one_or_none()

    @staticmethod
    def create_article(db: Session, article_data: dict):
        db_article = Article(**article_data)
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def update_article(db: Session, article_id: str, article_update: ArticleUpdate):
        article = db.execute(select(Article).filter_by(id=article_id)).scalar_one_or_none()
        if not article:
            return None
        update_data = article_update.dict(exclude_unset=True)
        db.execute(
            update(Article).where(Article.id == article_id).values(**update_data)
        )
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def approve_article(db: Session, article_id: str):
        article = db.execute(select(Article).filter_by(id=article_id)).scalar_one_or_none()
        if not article:
            return None
        db.execute(
            update(Article).where(Article.id == article_id).values(status=ArticleStatus.PUBLISHED)
        )
        db.commit()
        db.refresh(article)
        return article
    
    @staticmethod
    def get_latest_articles(db: Session):
        return db.execute(
            select(Article)
            .filter_by(status=ArticleStatus.PUBLISHED)
            .order_by(Article.date.desc())  # Newest first
        ).scalars().all()
        
    @staticmethod
    def get_popular_articles(db: Session, limit: int = 10):
        return db.execute(
            select(Article)
            .filter_by(status=ArticleStatus.PUBLISHED)
            .order_by(Article.no_of_readers.desc())
            .limit(limit)
        ).scalars().all()

    @staticmethod
    def get_popular_articles_last_week(db: Session, limit: int = 10):
        # Calculate date 7 days ago
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        one_week_ago_str = one_week_ago.date().isoformat()
        
        return db.execute(
            select(Article)
            .filter(
                Article.status == ArticleStatus.PUBLISHED,
                Article.date >= one_week_ago_str
            )
            .order_by(Article.no_of_readers.desc())
            .limit(limit)
        ).scalars().all()