from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.article import ArticleService
from app.schemas.article import Article, ArticlePreview, ArticleCreate, ArticleUpdate
from app.models.user import User, Role
from app.dependencies import get_current_user, get_optional_user, require_role
from fastapi import Query
from app.services.subscription import SubscriptionService
from app.core.cloudinary_config import cloudinary
import cloudinary.uploader
import json


router = APIRouter(prefix="/articles", tags=["articles"])

# ===== All Articles with Filters =====
@router.get("/", response_model=List[Article])
async def get_all_articles(
    status: Optional[str] = Query(None, description="Filter by article status (DRAFT, REVIEW, PUBLISHED)"),
    author: Optional[str] = Query(None, description="Filter by author ID"),
    tag: Optional[str] = Query(None, description="Filter by tag keyword"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get all articles with optional filters
    - Published articles are public.
    - Unpublished articles require the user to be the author or an editor/admin.
    """
    articles = ArticleService.get_all_articles(db, status=status, author=author, tag=tag)

    # Filter unpublished articles
    if current_user is None:
        articles = [a for a in articles if a.status == "PUBLISHED"]
    else:
        def can_view(article):
            return (
                article.status == "PUBLISHED" or
                article.author == current_user.id or
                current_user.role in [Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]
            )
        articles = list(filter(can_view, articles))

    return articles

# ===== Latest Published Articles =====
@router.get("/latest", response_model=List[ArticlePreview])
async def get_latest_articles(db: Session = Depends(get_db)):
    """Get latest published articles"""
    articles = ArticleService.get_latest_articles(db)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    return articles

@router.get("/popular", response_model=List[ArticlePreview])
async def get_popular_articles(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of articles to return", gt=0, le=50)
):
    """Get most popular articles"""
    articles = ArticleService.get_popular_articles(db, limit)
    if not articles:
        raise HTTPException(status_code=404, detail="No popular articles found")
    return articles

@router.get("/popular/week", response_model=List[ArticlePreview])
async def get_popular_articles_last_week(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of articles to return", gt=0, le=50)
):
    """Get popular articles from last week"""
    articles = ArticleService.get_popular_articles_last_week(db, limit)
    return articles or []

# ===== Parameterized Path Endpoints =====
@router.get("/{category}", response_model=List[ArticlePreview])
async def get_articles_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    """Get articles by category"""
    articles = ArticleService.get_articles_by_category(db, category)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this category")
    return articles

@router.get("/{category}/{subcategory}", response_model=List[ArticlePreview])
async def get_articles_by_subcategory(
    category: str,
    subcategory: str,
    db: Session = Depends(get_db)
):
    """Get articles by subcategory"""
    articles = ArticleService.get_articles_by_subcategory(db, category, subcategory)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this subcategory")
    return articles

@router.get("/{category}/{subcategory}/{slug}", response_model=Article)
async def get_article_by_slug(
    category: str,
    subcategory: str,
    slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get single article by slug"""
    article = ArticleService.get_article_by_slug(db, category, subcategory, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Premium content check
    if article.is_premium:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication required for premium content"
            )
        
        # Allow admin/editor roles to bypass subscription
        if current_user.role not in [Role.ADMIN, Role.EDITOR, Role.SUPERADMIN]:
            # Check subscription status
            subscription = SubscriptionService.get_user_subscription_status(db, current_user.id)
            if not subscription.get("is_active", False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Active subscription required for premium content"
                )
    
    return article

# ===== Protected Endpoints =====
@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.WRITER, Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]))
):
    """Create new article with image upload to Cloudinary"""
    try:
        # Upload image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file, folder="ensight_articles")
        image_url = upload_result.get("secure_url")
        if not image_url:
            raise Exception("Cloudinary did not return a secure_url")

        # Parse and prepare article data
        data = json.loads(article_data)
        data["image"] = image_url
        data["author"] = current_user.id

        new_article = ArticleService.create_article(db, data)
        return new_article

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create article: {str(e)}")

@router.patch("/{id}", response_model=Article)
async def update_article(
    id: str,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update existing article"""
    article = ArticleService.get_article_by_id(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Authorization check
    if article.author != current_user.id and current_user.role not in [Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this article"
        )
    
    updated_article = ArticleService.update_article(db, id, article_update)
    return updated_article

@router.patch("/{id}/approve", response_model=Article)
async def approve_article(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([Role.EDITOR, Role.ADMIN, Role.SUPERADMIN]))
):
    """Approve article for publishing"""
    article = ArticleService.approve_article(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article