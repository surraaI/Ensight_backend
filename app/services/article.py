from sqlalchemy.orm import Session, load_only
from sqlalchemy import select, update, func
from app.models.article import Article, ArticleStatus
from app.schemas.article import ArticleCreate, ArticleUpdate
from datetime import datetime, timedelta
import slugify

class ArticleService:
    # Common columns for previews
    PREVIEW_COLUMNS = [
        Article.id,
        Article.slug,
        Article.title,
        Article.category,
        Article.subcategory,
        Article.author,
        Article.status,
        Article.content,
        Article.date,
        Article.read_time,
        Article.no_of_readers,
        Article.image,
        Article.description,
        Article.is_premium,
        Article.no_of_readers,
        Article.href  # Added href field
    ]

    @staticmethod
    def get_articles_by_category(db: Session, category: str):
        return db.execute(
            select(Article)
            .options(load_only(*ArticleService.PREVIEW_COLUMNS))
            .filter(
                func.lower(Article.category) == category.lower(),
                Article.status == ArticleStatus.PUBLISHED
            )
        ).scalars().all()

    @staticmethod
    def get_articles_by_subcategory(db: Session, category: str, subcategory: str):
        return db.execute(
            select(Article)
            .options(load_only(*ArticleService.PREVIEW_COLUMNS))
            .filter(
                func.lower(Article.category) == category.lower(),
                func.lower(Article.subcategory) == subcategory.lower(),
                Article.status == ArticleStatus.PUBLISHED
            )
        ).scalars().all()

    @staticmethod
    def get_article_by_slug(db: Session, category: str, subcategory: str, slug: str):
        return db.execute(
            select(Article).filter(
                func.lower(Article.category) == category.lower(),
                func.lower(Article.subcategory) == subcategory.lower(),
                Article.slug == slug,
                Article.status == ArticleStatus.PUBLISHED
            )
        ).scalar_one_or_none()

    @staticmethod
    def get_article_by_id(db: Session, article_id: str):
        return db.execute(select(Article).filter_by(id=article_id)).scalar_one_or_none()

    @staticmethod
    def create_article(db: Session, article_data: dict):
        # Generate slug if not provided
        if not article_data.get("slug") and article_data.get("title"):
            article_data["slug"] = slugify.slugify(article_data["title"])
        
        # Lowercase category/subcategory
        if "category" in article_data:
            article_data["category"] = article_data["category"].lower()
        if "subcategory" in article_data:
            article_data["subcategory"] = article_data["subcategory"].lower()

        # Generate href from slug if missing
        if not article_data.get("href") and article_data.get("slug"):
            article_data["href"] = f"/{article_data.get('category', '')}/" \
                                f"{article_data.get('subcategory', '')}/" \
                                f"{article_data['slug']}"

        db_article = Article(**article_data)
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article


    @staticmethod
    def update_article(db: Session, article_id: str, article_update: ArticleUpdate):
        article = ArticleService.get_article_by_id(db, article_id)
        if not article:
            return None
        
        update_data = article_update.dict(exclude_unset=True)
        
        # Handle slug generation if title is updated
        if 'title' in update_data and 'slug' not in update_data:
            update_data['slug'] = slugify.slugify(update_data['title'])
        
        # Handle category/subcategory lowercase conversion
        for field in ['category', 'subcategory']:
            if field in update_data:
                update_data[field] = update_data[field].lower()
        
        # Regenerate href if slug or categories change
        if any(field in update_data for field in ['slug', 'category', 'subcategory']):
            category = update_data.get('category', article.category)
            subcategory = update_data.get('subcategory', article.subcategory)
            slug = update_data.get('slug', article.slug)
            update_data['href'] = f"/{category}/{subcategory}/{slug}"
        
        db.execute(
            update(Article).where(Article.id == article_id).values(**update_data)
        )
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def approve_article(db: Session, article_id: str):
        article = ArticleService.get_article_by_id(db, article_id)
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
            .options(load_only(*ArticleService.PREVIEW_COLUMNS))
            .filter_by(status=ArticleStatus.PUBLISHED)
            .order_by(Article.date.desc())
        ).scalars().all()
        
    @staticmethod
    def get_popular_articles(db: Session, limit: int = 10):
        return db.execute(
            select(Article)
            .options(load_only(*ArticleService.PREVIEW_COLUMNS))
            .filter_by(status=ArticleStatus.PUBLISHED)
            .order_by(Article.no_of_readers.desc())
            .limit(limit)
        ).scalars().all()

    @staticmethod
    def get_popular_articles_last_week(db: Session, limit: int = 10):
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        return db.execute(
            select(Article)
            .options(load_only(*ArticleService.PREVIEW_COLUMNS))
            .filter(
                Article.status == ArticleStatus.PUBLISHED,
                Article.date >= one_week_ago
            )
            .order_by(Article.no_of_readers.desc())
            .limit(limit)
        ).scalars().all()